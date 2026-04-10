from agent.router import handle_user_query


def main():
    print("=== FETCHING RELEVANT ROLES ===")

    query = input("What job are you looking for? ")
    skills = input("Enter your skills (comma-separated): ")

    skills_list = [s.strip() for s in skills.split(",")]

    handle_user_query(query, skills_list)


if __name__ == "__main__":
    main()