from calender_service import create_calendar_event


if __name__ == "__main__":
    link = create_calendar_event("Crocin", "16:00")
    print(link)