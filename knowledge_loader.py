import os

# Cache for loaded knowledge
knowledge_cache = {}

def load_knowledge(language):

    # Return cached version if already loaded
    if language in knowledge_cache:
        return knowledge_cache[language]

    knowledge = ""

    folder = os.path.join("Knowledge", language)

    print("Loading knowledge from:", folder)

    if not os.path.exists(folder):
        print("Language folder not found!")
        return ""

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if os.path.isfile(path):

            print("Loading:", file)

            with open(path, "r", encoding="utf-8") as f:

                knowledge += f.read()
                knowledge += "\n\n"

    # Save in memory
    knowledge_cache[language] = knowledge

    print(f"{language} knowledge cached successfully")

    return knowledge