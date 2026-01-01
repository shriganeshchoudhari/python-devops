def pagination_simulator():
    # Pretend API responses
    pages = [
        ["item1", "item2"],
        ["item3", "item4"],
        ["item5"]
    ]

    all_items = []
    for page in pages:
        all_items.extend(page)

    print("Total items collected:", len(all_items))
    print("Items:", all_items)


if __name__ == "__main__":
    pagination_simulator()