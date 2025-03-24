import win32com.client
import os

outlook = win32com.client.Dispatch('outlook.application')
namespace = outlook.GetNamespace("MAPI")
date = "05-03-2025"

inbox = namespace.GetDefaultFolder(6)


save_dir = os.path.join(os.getcwd(), 'Mail_bills')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

messages = inbox.Items
for msg in messages:
    try:
        if f"Your bill details : {date}" in msg.Subject and msg.SenderEmailAddress == "ebill.mumbaielectricity@adanielectricity.co":
            print(f"Processing: {msg.Subject} - {msg.ReceivedTime}")

            for atch in msg.Attachments:
                save_path = os.path.join(save_dir, atch.FileName)

                # Ensure the directory exists
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                atch.SaveAsFile(save_path)
                print(f"Saved: {atch.FileName} to {save_path}")

    except Exception as e:
        print(f"Error processing email: {e}")

print("Download complete.")



