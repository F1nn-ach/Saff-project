from saff_project.config import Config
from saff_project.providers.ollama import OllamaLLM


def main():
    config = Config.load()
    if not config.ollama:
        print("ไม่พบ config ของ ollama")
        return


    llm = OllamaLLM(config.ollama)

    while True:
        try:
            user_msg = input("\nYou > ").strip()

            if not user_msg:
                continue

            if user_msg.lower() in ["exit", "quit", "q"]:
                print("See ya!")
                break

            reply = llm.chat(user_msg)
            print(f"\nSaff > {reply}")

        except (KeyboardInterrupt, EOFError):
            print("\nSee ya!")
            break


if __name__ == "__main__":
    main()
