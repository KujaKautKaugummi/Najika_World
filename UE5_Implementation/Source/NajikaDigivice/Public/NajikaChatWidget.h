// Copyright Claude Code. All Rights Reserved.

#pragma once

#include "CoreMinimal.h"
#include "Blueprint/UserWidget.h"
#include "NajikaBackendTypes.h"
#include "NajikaChatWidget.generated.h"

class UScrollBox;
class UEditableTextBox;
class UButton;
class UTextBlock;
class UVerticalBox;
class UNajikaHttpClient;

/**
 * Chat Widget for Najika Digivice
 *
 * Features:
 * - Scrollable chat history
 * - Message input with send button
 * - User/Najika message differentiation
 * - Typing indicator
 * - Voice call toggle button
 * - Message timestamps
 * - Character limit indicator
 * - Auto-scroll to bottom
 *
 * Usage:
 * - Create Blueprint child class (WBP_NajikaChat)
 * - Bind UI elements via meta=(BindWidget)
 * - Show/hide via PlayerController
 */
UCLASS()
class NAJIKADIGIVICE_API UNajikaChatWidget : public UUserWidget
{
	GENERATED_BODY()

public:
	virtual void NativeConstruct() override;

	// ============================================================
	// CHAT UI ELEMENTS
	// ============================================================

	/** Chat history scroll box */
	UPROPERTY(meta = (BindWidget))
	UScrollBox* ChatHistoryScrollBox;

	/** Message input box */
	UPROPERTY(meta = (BindWidget))
	UEditableTextBox* MessageInputBox;

	/** Send button */
	UPROPERTY(meta = (BindWidget))
	UButton* SendButton;

	/** Voice call toggle button */
	UPROPERTY(meta = (BindWidget))
	UButton* VoiceCallButton;

	/** Voice call indicator text */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* VoiceCallStatusText;

	/** Typing indicator (visible when Najika is typing) */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* TypingIndicatorText;

	/** Character count text (e.g., "120/500") */
	UPROPERTY(meta = (BindWidget))
	UTextBlock* CharacterCountText;

	// ============================================================
	// SETTINGS
	// ============================================================

	/** Max message length */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Chat")
	int32 MaxMessageLength = 500;

	/** Auto-scroll to bottom on new message */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Chat")
	bool bAutoScrollToBottom = true;

	/** Show timestamps */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Chat")
	bool bShowTimestamps = true;

	// ============================================================
	// MESSAGE TEMPLATES (for Blueprint)
	// ============================================================

	/** User message widget class */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Chat")
	TSubclassOf<UUserWidget> UserMessageWidgetClass;

	/** Najika message widget class */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Najika|Chat")
	TSubclassOf<UUserWidget> NajikaMessageWidgetClass;

	// ============================================================
	// FUNCTIONS
	// ============================================================

	/**
	 * Send chat message to Najika
	 * @param Message User message text
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void SendMessage(const FString& Message);

	/**
	 * Add user message to chat history
	 * @param Message Message text
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void AddUserMessage(const FString& Message);

	/**
	 * Add Najika response to chat history
	 * @param Message Message text
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void AddNajikaMessage(const FString& Message);

	/**
	 * Clear chat history
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void ClearChatHistory();

	/**
	 * Load chat history from backend
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void LoadChatHistory();

	/**
	 * Toggle voice call
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void ToggleVoiceCall();

	/**
	 * Show typing indicator
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void ShowTypingIndicator(bool bShow);

	/**
	 * Scroll to bottom of chat
	 */
	UFUNCTION(BlueprintCallable, Category = "Najika|Chat")
	void ScrollToBottom();

protected:
	// Button handlers
	UFUNCTION()
	void OnSendButtonClicked();

	UFUNCTION()
	void OnVoiceCallButtonClicked();

	UFUNCTION()
	void OnMessageInputTextChanged(const FText& Text);

	UFUNCTION()
	void OnMessageInputTextCommitted(const FText& Text, ETextCommit::Type CommitMethod);

	// Backend callbacks
	UFUNCTION()
	void OnChatResponseReceived(FString Response, FNajikaState NajikaState, FNajikaLivingState LivingState);

	UFUNCTION()
	void OnChatHistoryReceived(FNajikaAPIResponse APIResponse);

	UFUNCTION()
	void OnVoiceCallToggled(bool bSuccess, FString Message);

	// Helper functions
	void UpdateCharacterCount();
	FString GetFormattedTimestamp() const;

	// Voice call state
	bool bIsVoiceCallActive = false;

	// Backend client reference
	UNajikaHttpClient* BackendClient = nullptr;
};
