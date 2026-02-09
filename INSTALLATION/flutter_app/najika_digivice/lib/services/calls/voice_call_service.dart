import 'package:flutter/foundation.dart';
import 'package:flutter_webrtc/flutter_webrtc.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;

import '../network/connection_manager.dart';
import '../../core/constants/app_constants.dart';

/// Voice Call Service
///
/// Handles WebRTC voice calls with:
/// - P2P encrypted audio
/// - TURN server relay (no direct IP exposure)
/// - End-to-end encryption
class VoiceCallService extends ChangeNotifier {
  static final VoiceCallService instance = VoiceCallService._();
  VoiceCallService._();

  // WebRTC
  RTCPeerConnection? _peerConnection;
  MediaStream? _localStream;
  MediaStream? _remoteStream;

  // Call state
  bool _isInCall = false;
  bool _isMuted = false;
  bool _isSpeakerOn = false;
  String? _currentCallId;
  String? _remoteUserId;

  // Signaling
  IO.Socket? _signalingSocket;

  // Getters
  bool get isInCall => _isInCall;
  bool get isMuted => _isMuted;
  bool get isSpeakerOn => _isSpeakerOn;
  MediaStream? get remoteStream => _remoteStream;

  /// Initialize voice call service
  Future<void> initialize() async {
    debugPrint('📞 VoiceCallService: Initializing...');

    // Connect to signaling server
    await _connectSignaling();

    debugPrint('✅ VoiceCallService: Initialized');
  }

  /// Connect to signaling server
  Future<void> _connectSignaling() async {
    final messengerUrl = ConnectionManager.instance.activeMessengerUrl ??
        AppConstants.messengerServerUrl;

    _signalingSocket = IO.io(
      messengerUrl,
      IO.OptionBuilder()
          .setTransports(['websocket'])
          .disableAutoConnect()
          .build(),
    );

    // Signaling handlers
    _signalingSocket!.on('call_offer', (data) {
      _handleCallOffer(data);
    });

    _signalingSocket!.on('call_answer', (data) {
      _handleCallAnswer(data);
    });

    _signalingSocket!.on('ice_candidate', (data) {
      _handleIceCandidate(data);
    });

    _signalingSocket!.on('call_ended', (data) {
      _handleCallEnded();
    });

    _signalingSocket!.connect();
  }

  /// Start outgoing call
  Future<void> startCall(String remoteUserId) async {
    debugPrint('📞 Starting call to: $remoteUserId');

    _remoteUserId = remoteUserId;
    _currentCallId = DateTime.now().millisecondsSinceEpoch.toString();

    // Get local audio stream
    _localStream = await navigator.mediaDevices.getUserMedia({
      'audio': {
        'echoCancellation': true,
        'noiseSuppression': true,
        'autoGainControl': true,
      },
      'video': false,
    });

    // Create peer connection
    await _createPeerConnection();

    // Add local stream
    _localStream!.getTracks().forEach((track) {
      _peerConnection!.addTrack(track, _localStream!);
    });

    // Create offer
    final offer = await _peerConnection!.createOffer();
    await _peerConnection!.setLocalDescription(offer);

    // Send offer via signaling
    _signalingSocket!.emit('call_offer', {
      'call_id': _currentCallId,
      'to': remoteUserId,
      'offer': offer.toMap(),
    });

    _isInCall = true;
    notifyListeners();

    debugPrint('✅ Call offer sent');
  }

  /// Handle incoming call offer
  Future<void> _handleCallOffer(dynamic data) async {
    debugPrint('📞 Incoming call offer');

    _remoteUserId = data['from'];
    _currentCallId = data['call_id'];

    // Get local audio stream
    _localStream = await navigator.mediaDevices.getUserMedia({
      'audio': {
        'echoCancellation': true,
        'noiseSuppression': true,
        'autoGainControl': true,
      },
      'video': false,
    });

    // Create peer connection
    await _createPeerConnection();

    // Add local stream
    _localStream!.getTracks().forEach((track) {
      _peerConnection!.addTrack(track, _localStream!);
    });

    // Set remote description
    final offer = RTCSessionDescription(
      data['offer']['sdp'],
      data['offer']['type'],
    );
    await _peerConnection!.setRemoteDescription(offer);

    // Create answer
    final answer = await _peerConnection!.createAnswer();
    await _peerConnection!.setLocalDescription(answer);

    // Send answer
    _signalingSocket!.emit('call_answer', {
      'call_id': _currentCallId,
      'to': _remoteUserId,
      'answer': answer.toMap(),
    });

    _isInCall = true;
    notifyListeners();

    debugPrint('✅ Call answer sent');
  }

  /// Handle call answer
  Future<void> _handleCallAnswer(dynamic data) async {
    debugPrint('📞 Call answer received');

    final answer = RTCSessionDescription(
      data['answer']['sdp'],
      data['answer']['type'],
    );

    await _peerConnection!.setRemoteDescription(answer);

    debugPrint('✅ Call established');
  }

  /// Handle ICE candidate
  Future<void> _handleIceCandidate(dynamic data) async {
    final candidate = RTCIceCandidate(
      data['candidate']['candidate'],
      data['candidate']['sdpMid'],
      data['candidate']['sdpMLineIndex'],
    );

    await _peerConnection!.addCandidate(candidate);
  }

  /// Create peer connection
  Future<void> _createPeerConnection() async {
    // STUN/TURN servers (prevents IP leaks)
    final configuration = {
      'iceServers': [
        {
          'urls': [
            'stun:stun.l.google.com:19302',
            'stun:stun1.l.google.com:19302',
          ]
        },
        // TODO: Add your own TURN server for relay
        // {
        //   'urls': 'turn:your-turn-server.com:3478',
        //   'username': 'username',
        //   'credential': 'password'
        // }
      ],
      'iceTransportPolicy': 'relay', // Force TURN relay (no direct P2P)
    };

    _peerConnection = await createPeerConnection(configuration);

    // ICE candidate handler
    _peerConnection!.onIceCandidate = (candidate) {
      if (candidate != null) {
        _signalingSocket!.emit('ice_candidate', {
          'call_id': _currentCallId,
          'to': _remoteUserId,
          'candidate': candidate.toMap(),
        });
      }
    };

    // Remote stream handler
    _peerConnection!.onTrack = (event) {
      debugPrint('📞 Remote track received');
      if (event.streams.isNotEmpty) {
        _remoteStream = event.streams[0];
        notifyListeners();
      }
    };

    // Connection state handler
    _peerConnection!.onConnectionState = (state) {
      debugPrint('📞 Connection state: $state');
      if (state == RTCPeerConnectionState.RTCPeerConnectionStateDisconnected ||
          state == RTCPeerConnectionState.RTCPeerConnectionStateFailed) {
        endCall();
      }
    };
  }

  /// Toggle mute
  void toggleMute() {
    if (_localStream != null) {
      final audioTrack = _localStream!.getAudioTracks()[0];
      audioTrack.enabled = !audioTrack.enabled;
      _isMuted = !audioTrack.enabled;
      notifyListeners();
      debugPrint('🔇 Mute: $_isMuted');
    }
  }

  /// Toggle speaker
  void toggleSpeaker() {
    _isSpeakerOn = !_isSpeakerOn;
    // Platform-specific speaker toggle
    Helper.setSpeakerphoneOn(_isSpeakerOn);
    notifyListeners();
    debugPrint('🔊 Speaker: $_isSpeakerOn');
  }

  /// End call
  Future<void> endCall() async {
    debugPrint('📞 Ending call');

    // Notify remote user
    if (_currentCallId != null && _remoteUserId != null) {
      _signalingSocket!.emit('call_ended', {
        'call_id': _currentCallId,
        'to': _remoteUserId,
      });
    }

    await _cleanup();

    _isInCall = false;
    _currentCallId = null;
    _remoteUserId = null;
    notifyListeners();

    debugPrint('✅ Call ended');
  }

  /// Handle call ended by remote user
  Future<void> _handleCallEnded() async {
    debugPrint('📞 Call ended by remote user');
    await _cleanup();
    _isInCall = false;
    _currentCallId = null;
    _remoteUserId = null;
    notifyListeners();
  }

  /// Cleanup resources
  Future<void> _cleanup() async {
    // Stop local stream
    if (_localStream != null) {
      _localStream!.getTracks().forEach((track) {
        track.stop();
      });
      await _localStream!.dispose();
      _localStream = null;
    }

    // Close peer connection
    if (_peerConnection != null) {
      await _peerConnection!.close();
      _peerConnection = null;
    }

    // Clear remote stream
    _remoteStream = null;

    _isMuted = false;
    _isSpeakerOn = false;
  }

  /// Dispose
  @override
  void dispose() {
    _cleanup();
    _signalingSocket?.disconnect();
    _signalingSocket?.dispose();
    super.dispose();
  }
}
