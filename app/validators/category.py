def category_validation(category: str) -> bool:
    category_list = ("Supermarkets", "Restaurants", "Clothes", "Medicine", "Transport", "Devices", "Education",
                     "Services", "Travel", "Housing", "Transfers", "Investments", "Hobby", "Jewelry", "Sale", "Salary",
                     "Other")
    if category in category_list:
        return True
    else:
        return False
