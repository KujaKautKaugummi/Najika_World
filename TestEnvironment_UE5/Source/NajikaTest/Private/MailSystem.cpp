// MailSystem.cpp
#include "MailSystem.h"
UMailSystem::UMailSystem() { PrimaryComponentTick.bCanEverTick = false; }
void UMailSystem::BeginPlay() { Super::BeginPlay(); }

bool UMailSystem::SendMail(const FMail& Mail) {
    // In real implementation, would send to server
    return true;
}

bool UMailSystem::DeleteMail(const FString& MailID) {
    for (int32 i = Inbox.Num() - 1; i >= 0; i--) {
        if (Inbox[i].MailID == MailID) {
            Inbox.RemoveAt(i);
            OnMailDeleted.Broadcast(MailID);
            return true;
        }
    }
    return false;
}

bool UMailSystem::ClaimAttachments(const FString& MailID) {
    for (FMail& Mail : Inbox) {
        if (Mail.MailID == MailID && Mail.HasAttachments) {
            AActor* Owner = GetOwner();
            if (Owner) {
                UInventoryComponent* Inventory = Owner->FindComponentByClass<UInventoryComponent>();
                if (Inventory) {
                    for (const FString& ItemID : Mail.AttachedItems) {
                        FItemData Item;
                        Item.ItemID = ItemID;
                        Inventory->AddItem(Item, 1);
                    }
                    if (Mail.AttachedGold > 0) Inventory->Gold += Mail.AttachedGold;
                }
            }
            Mail.HasAttachments = false;
            Mail.AttachedItems.Empty();
            Mail.AttachedGold = 0;
            OnAttachmentsClaimed.Broadcast(MailID);
            return true;
        }
    }
    return false;
}

TArray<FMail> UMailSystem::GetUnreadMail() const {
    TArray<FMail> Unread;
    for (const FMail& Mail : Inbox) {
        if (!Mail.bIsRead) Unread.Add(Mail);
    }
    return Unread;
}
