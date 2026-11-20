from chile_datainnovacion_sdk import ChileDataInnovacionClient


def main() -> None:
    with ChileDataInnovacionClient() as client:
        projects = client.projects.list(limit=5)
        for project in projects:
            print(project.code, project.project_title)


if __name__ == "__main__":
    main()
