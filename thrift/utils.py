CHOICES = {
    'building':
        (("1", "1"), ("2", "2")),
    'floor': 
        (("B", "B"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), 
        ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"),
        ("10", "10"), ("11", "11"), ("12", "12"), ("R", "R")),
    'condition':
        (("New", "New"), ("Like New", "Like New"), ("Good", "Good"),
        ("Fair", "Fair"), ("Poor", "Poor")),
    'item-type':
        (("Clothes", "Clothes"), ("Kitchen", "Kitchen"),
        ("Furniture", "Furniture"), ("Sporting", "Sporting"), 
        ("Fitness", "Fitness"), ("Art", "Art"), ("Misc", "Misc")),
    'sale-status':
        (("available", "available"), ("pending", "pending"), ("sold", "sold"))
}

def item_image_upload_handler(instance, filename):
    file_prefix = str(uuid.uuid1()) # uuid1 -> uuid + timestamps
    return f"images{file_prefix}-{filename}" # creates a new file path for the upload upload adding the uuid to its original name

def get_item_types_list():
    """return list of item types listed in choices"""
    types = []
    for type in CHOICES["item-type"]:
        types.append(type[0])
    return types