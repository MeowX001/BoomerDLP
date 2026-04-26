import os

# ===== Create download folder if it doesn't exist =====
if not os.path.exists("download"):
    os.makedirs("download")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def run_command(cmd, use_local):
    """Run yt-dlp command using local exe or system-installed and save to download folder"""
    # Make sure output goes to "download" folder with proper filename
    output_path = os.path.join(os.getcwd(), "download", "%(title)s.%(ext)s")
    cmd = f'{cmd} -o "{output_path}"'

    if use_local:
        cmd = cmd.replace("yt-dlp", "yt-dlp.exe")
    os.system(cmd)

def audio_menu(url, use_local):
    while True:
        clear()
        print("==== AUDIO MENU ====")
        print("1. M4A (best audio)")
        print("2. MP3")
        print("3. Back")

        choice = input("Select option (1-3): ")

        if choice == "1":
            run_command(f'yt-dlp -f bestaudio "{url}"', use_local)
        elif choice == "2":
            run_command(f'yt-dlp -f bestaudio -x --audio-format mp3 "{url}"', use_local)
        elif choice == "3":
            return
        else:
            print("Invalid choice")

        input("Press Enter to continue...")

def video_menu(url, use_local):
    while True:
        clear()
        print("==== VIDEO MENU ====")
        print("1. MP4")
        print("2. MP4 (1080p)")
        print("3. WEBM")
        print("4. WEBM (1080p)")
        print("5. MKV")
        print("6. MKV (1080p)")
        print("7. Back")

        choice = input("Select option (1-7): ")

        if choice == "1":
            run_command(f'yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]" "{url}"', use_local)
        elif choice == "2":
            run_command(f'yt-dlp -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4]" "{url}"', use_local)
        elif choice == "3":
            run_command(f'yt-dlp -f "bv*[ext=webm]+ba[ext=webm]/b[ext=webm]" "{url}"', use_local)
        elif choice == "4":
            run_command(f'yt-dlp -f "bv*[height<=1080][ext=webm]+ba[ext=webm]/b[height<=1080][ext=webm]" "{url}"', use_local)
        elif choice == "5":
            run_command(f'yt-dlp -f "bv+ba/b" --merge-output-format mkv "{url}"', use_local)
        elif choice == "6":
            run_command(f'yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]" --merge-output-format mkv "{url}"', use_local)
        elif choice == "7":
            return
        else:
            print("Invalid choice")

        input("Press Enter to continue...")

def main():
    clear()
    print("==== YT-DLP TOOL ====")
    print("Do you have yt-dlp installed? (y/n)")
    installed = input(">>> ").lower()
    use_local = installed != "y"  # True if user does NOT have yt-dlp installed

    while True:
        clear()
        print("==== MAIN MENU ====")
        print("1. Update")
        print("2. Audio")
        print("3. Video")
        print("4. Exit")
        print("5. Info")

        choice = input("Select option (1-5): ")

        if choice == "1":
            run_command("yt-dlp -U", use_local)
            input("Press Enter to continue...")

        elif choice == "2":
            url = input("Enter URL: ")
            audio_menu(url, use_local)

        elif choice == "3":
            url = input("Enter URL: ")
            video_menu(url, use_local)

        elif choice == "4":
            print("Exiting...")
            break

        elif choice == "5":
            clear()
            print("==== INFO ====")
            print("Made by Mr. GPT and meowx001")
            print("Make sure you have a stable internet before downloading")
            print("If downloading does not work, try updating yt-dlp")
            input("\nPress Enter to go back...")

        else:
            print("Invalid choice")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 
    