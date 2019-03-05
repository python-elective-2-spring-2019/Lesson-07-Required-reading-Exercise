import script
import subpro
import dircontent


# Start script


def main():
    subpro.clone_all_repos(script.real_list)
    dircontent.create_curriculum_list()

if __name__ == "__main__":
    main()
