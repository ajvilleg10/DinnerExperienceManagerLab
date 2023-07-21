from dining_experience_manager import DiningExperienceManager

if __name__ == "__main__":
    manager = DiningExperienceManager()
    total_cost = manager.process_order()
    if total_cost != -1:
        print("Thank you for your order! Enjoy your meal.")
