// Copyright Claude Code. All Rights Reserved.

#include "NajikaChatWidget.h"
#include "Components/ScrollBox.h"
#include "Components/EditableTextBox.h"
#include "Components/Button.h"
#include "Components/TextBlock.h"
#include "Components/VerticalBox.h"
#include "NajikaHttpClient.h"
#include "NajikaCharacter.h"
#include "Kismet/GameplayStatics.h"
#include "JsonObjectConverter.h"

void UNajikaChatWidget::NativeConstruct()
{
	Super::NativeConstruct();

	UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] Chat widget initialized"));

	// Bind button events
	if (SendButton)
	{
		SendButton->OnClicked.AddDynamic(this, &UNajikaChatWidget::OnSendButtonClicked);
	}

	if (VoiceCallButton)
	{
		VoiceCallButton->OnClicked.AddDynamic(this, &UNajikaChatWidget::OnVoiceCallButtonClicked);
	}

	// Bind message input events
	if (MessageInputBox)
	{
		MessageInputBox->OnTextChanged.AddDynamic(this, &UNajikaChatWidget::OnMessageInputTextChanged);
		MessageInputBox->OnTextCommitted.AddDynamic(this, &UNajikaChatWidget::OnMessageInputTextCommitted);
	}

	// Hide typing indicator by default
	ShowTypingIndicator(false);

	// Update character count
	UpdateCharacterCount();

	// Get backend client from Character
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika)
		{
			BackendClient = Najika->BackendClient;
		}
	}

	// Load chat history on construct
	LoadChatHistory();
}

// ============================================================
// MESSAGE SENDING
// ============================================================

void UNajikaChatWidget::SendMessage(const FString& Message)
{
	if (Message.IsEmpty())
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaChatWidget] Cannot send empty message"));
		return;
	}

	if (Message.Len() > MaxMessageLength)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaChatWidget] Message too long (%d > %d)"), Message.Len(), MaxMessageLength);
		return;
	}

	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaChatWidget] Backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] Sending message: %s"), *Message);

	// Add user message to chat history
	AddUserMessage(Message);

	// Show typing indicator
	ShowTypingIndicator(true);

	// Send to backend
	FOnNajikaChatResponse Delegate;
	Delegate.BindDynamic(this, &UNajikaChatWidget::OnChatResponseReceived);
	BackendClient->SendChatMessage(Message, Delegate);

	// Clear input box
	if (MessageInputBox)
	{
		MessageInputBox->SetText(FText::GetEmpty());
	}

	UpdateCharacterCount();
}

void UNajikaChatWidget::AddUserMessage(const FString& Message)
{
	if (!ChatHistoryScrollBox)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaChatWidget] ChatHistoryScrollBox not bound"));
		return;
	}

	// Create user message widget (Blueprint implementation)
	if (UserMessageWidgetClass)
	{
		UUserWidget* MessageWidget = CreateWidget<UUserWidget>(GetWorld(), UserMessageWidgetClass);
		if (MessageWidget)
		{
			// Set message text (Blueprint should expose a function to set text)
			// For now, log it
			UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] User message added: %s"), *Message);

			ChatHistoryScrollBox->AddChild(MessageWidget);
		}
	}
	else
	{
		// Fallback: Create simple text block
		UTextBlock* MessageText = NewObject<UTextBlock>(this);
		if (MessageText)
		{
			FString DisplayText = bShowTimestamps
				? FString::Printf(TEXT("[%s] User: %s"), *GetFormattedTimestamp(), *Message)
				: FString::Printf(TEXT("User: %s"), *Message);

			MessageText->SetText(FText::FromString(DisplayText));
			MessageText->SetColorAndOpacity(FSlateColor(FLinearColor(0.5f, 0.8f, 1.0f))); // Light blue
			ChatHistoryScrollBox->AddChild(MessageText);
		}
	}

	// Auto-scroll to bottom
	if (bAutoScrollToBottom)
	{
		ScrollToBottom();
	}
}

void UNajikaChatWidget::AddNajikaMessage(const FString& Message)
{
	if (!ChatHistoryScrollBox)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaChatWidget] ChatHistoryScrollBox not bound"));
		return;
	}

	// Create Najika message widget (Blueprint implementation)
	if (NajikaMessageWidgetClass)
	{
		UUserWidget* MessageWidget = CreateWidget<UUserWidget>(GetWorld(), NajikaMessageWidgetClass);
		if (MessageWidget)
		{
			UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] Najika message added: %s"), *Message);
			ChatHistoryScrollBox->AddChild(MessageWidget);
		}
	}
	else
	{
		// Fallback: Create simple text block
		UTextBlock* MessageText = NewObject<UTextBlock>(this);
		if (MessageText)
		{
			FString DisplayText = bShowTimestamps
				? FString::Printf(TEXT("[%s] Najika: %s"), *GetFormattedTimestamp(), *Message)
				: FString::Printf(TEXT("Najika: %s"), *Message);

			MessageText->SetText(FText::FromString(DisplayText));
			MessageText->SetColorAndOpacity(FSlateColor(FLinearColor(1.0f, 0.6f, 0.8f))); // Pink
			ChatHistoryScrollBox->AddChild(MessageText);
		}
	}

	// Auto-scroll to bottom
	if (bAutoScrollToBottom)
	{
		ScrollToBottom();
	}
}

// ============================================================
// CHAT HISTORY
// ============================================================

void UNajikaChatWidget::ClearChatHistory()
{
	if (ChatHistoryScrollBox)
	{
		ChatHistoryScrollBox->ClearChildren();
		UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] Chat history cleared"));
	}
}

void UNajikaChatWidget::LoadChatHistory()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaChatWidget] Cannot load history - backend client not initialized"));
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] Loading chat history from backend..."));

	FOnNajikaHTTPResponse Delegate;
	Delegate.BindDynamic(this, &UNajikaChatWidget::OnChatHistoryReceived);
	BackendClient->GetChatHistory(Delegate);
}

// ============================================================
// VOICE CALL
// ============================================================

void UNajikaChatWidget::ToggleVoiceCall()
{
	if (!BackendClient)
	{
		UE_LOG(LogTemp, Error, TEXT("[NajikaChatWidget] Backend client not initialized"));
		return;
	}

	FOnNajikaActionResponse Delegate;
	Delegate.BindDynamic(this, &UNajikaChatWidget::OnVoiceCallToggled);

	if (bIsVoiceCallActive)
	{
		// End voice call
		BackendClient->EndVoiceCall(Delegate);
	}
	else
	{
		// Start voice call
		BackendClient->StartVoiceCall(Delegate);
	}
}

// ============================================================
// UI HELPERS
// ============================================================

void UNajikaChatWidget::ShowTypingIndicator(bool bShow)
{
	if (TypingIndicatorText)
	{
		TypingIndicatorText->SetVisibility(bShow ? ESlateVisibility::Visible : ESlateVisibility::Collapsed);

		if (bShow)
		{
			TypingIndicatorText->SetText(FText::FromString(TEXT("Najika tippt...")));
		}
	}
}

void UNajikaChatWidget::ScrollToBottom()
{
	if (ChatHistoryScrollBox)
	{
		ChatHistoryScrollBox->ScrollToEnd();
	}
}

void UNajikaChatWidget::UpdateCharacterCount()
{
	if (!CharacterCountText || !MessageInputBox) return;

	int32 CurrentLength = MessageInputBox->GetText().ToString().Len();
	CharacterCountText->SetText(FText::FromString(FString::Printf(TEXT("%d/%d"), CurrentLength, MaxMessageLength)));

	// Change color based on length
	if (CurrentLength > MaxMessageLength * 0.9f)
	{
		CharacterCountText->SetColorAndOpacity(FSlateColor(FLinearColor::Red));
	}
	else if (CurrentLength > MaxMessageLength * 0.75f)
	{
		CharacterCountText->SetColorAndOpacity(FSlateColor(FLinearColor::Yellow));
	}
	else
	{
		CharacterCountText->SetColorAndOpacity(FSlateColor(FLinearColor::White));
	}
}

FString UNajikaChatWidget::GetFormattedTimestamp() const
{
	FDateTime Now = FDateTime::Now();
	return Now.ToString(TEXT("%H:%M:%S"));
}

// ============================================================
// BUTTON HANDLERS
// ============================================================

void UNajikaChatWidget::OnSendButtonClicked()
{
	if (MessageInputBox)
	{
		FString Message = MessageInputBox->GetText().ToString().TrimStartAndEnd();
		SendMessage(Message);
	}
}

void UNajikaChatWidget::OnVoiceCallButtonClicked()
{
	ToggleVoiceCall();
}

void UNajikaChatWidget::OnMessageInputTextChanged(const FText& Text)
{
	UpdateCharacterCount();
}

void UNajikaChatWidget::OnMessageInputTextCommitted(const FText& Text, ETextCommit::Type CommitMethod)
{
	// Send message on Enter key press
	if (CommitMethod == ETextCommit::OnEnter)
	{
		FString Message = Text.ToString().TrimStartAndEnd();
		SendMessage(Message);
	}
}

// ============================================================
// BACKEND CALLBACKS
// ============================================================

void UNajikaChatWidget::OnChatResponseReceived(FString Response, FNajikaState NajikaState, FNajikaLivingState LivingState)
{
	UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] Najika response: %s"), *Response);

	// Hide typing indicator
	ShowTypingIndicator(false);

	// Add Najika's response to chat
	AddNajikaMessage(Response);

	// Update character state (delegate to Character)
	APlayerController* PC = GetOwningPlayer();
	if (PC)
	{
		ANajikaCharacter* Najika = Cast<ANajikaCharacter>(PC->GetPawn());
		if (Najika)
		{
			Najika->CurrentState = NajikaState;
			Najika->LivingState = LivingState;
		}
	}
}

void UNajikaChatWidget::OnChatHistoryReceived(FNajikaAPIResponse APIResponse)
{
	if (!APIResponse.bSuccess)
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaChatWidget] Failed to load chat history: %s"), *APIResponse.ErrorMessage);
		return;
	}

	UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] Chat history loaded"));

	// Parse JSON data and populate chat history
	// TODO: Parse APIResponse.Data (JSON array of messages)
	// For now, just log success
}

void UNajikaChatWidget::OnVoiceCallToggled(bool bSuccess, FString Message)
{
	if (bSuccess)
	{
		bIsVoiceCallActive = !bIsVoiceCallActive;

		if (VoiceCallStatusText)
		{
			VoiceCallStatusText->SetText(FText::FromString(
				bIsVoiceCallActive ? TEXT("📞 Anruf aktiv") : TEXT("📞 Anruf beenden")
			));
		}

		UE_LOG(LogTemp, Log, TEXT("[NajikaChatWidget] Voice call %s"), bIsVoiceCallActive ? TEXT("started") : TEXT("ended"));
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("[NajikaChatWidget] Voice call toggle failed: %s"), *Message);
	}
}
