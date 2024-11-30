class Person:
    def __init__(self):
        self.name = ""
        self.age = 0
        self.gender = False
        self.height = 0
        self.child = None
        self.sibling = None

    def get_data(self):
        self.name = input("Enter name: ").strip()
        while True:
            try:
                self.age = int(input("Enter age: "))
                if self.age <= 0:
                    raise ValueError("Age must be a positive number.")
                break
            except ValueError as e:
                print(e)
        while True:
            sex = input("Enter the gender (m/f): ").strip().lower()
            if sex in ('m', 'f'):
                self.gender = True if sex == 'm' else False
                break
            else:
                print("Invalid input. Please enter 'm' or 'f'.")
        print()


class FamilyTree:
    def __init__(self):
        self.root = None
        self.is_root_set = False

    def add_new_person(self):
        temp = Person()
        temp.get_data()
        if self.root is None:
            self.root = temp
            self.is_root_set = True
        else:
            related_name = input("\nEnter the name of the related person: ").strip()
            print(f"\n1. Child\n2. Sibling")
            try:
                relationship = int(input(f"Enter the relationship type for {temp.name} with {related_name}: "))
            except ValueError:
                print("Invalid input. Person isn't added.\n")
                return

            related_person = self.search(related_name)
            if related_person is None:
                print("Related person not found. Person isn't added.\n")
                return

            if relationship == 1:
                self.add_child(related_person, temp)
            elif relationship == 2:
                self.add_sibling(related_person, temp)
            else:
                print("Invalid choice. Person isn't added.\n")
                return
        print("\nPerson added successfully.\n")

    def add_sibling(self, person1, person2):
        while person1.sibling:
            person1 = person1.sibling
        person1.sibling = person2
        person2.height = person1.height

    def add_child(self, person1, person2):
        if person1.child is None:
            person1.child = person2
        else:
            self.add_sibling(person1.child, person2)
        person2.height = person1.height + 1

    def search(self, name):
        if not self.root:
            print("Tree is empty.")
            return None
        return self.search_helper(self.root, name)

    def search_helper(self, current, name):
        if not current:
            return None
        if current.name == name:
            return current
        child_result = self.search_helper(current.child, name)
        if child_result:
            return child_result
        return self.search_helper(current.sibling, name)

    def display_tree(self, person, level=0):
        if not person:
            return
        gender = "Male" if person.gender else "Female"
        print("  " * level + f"|-- {person.name} (Age: {person.age}, Gender: {gender})")
        self.display_tree(person.child, level + 1)
        self.display_tree(person.sibling, level)

    def delete_tree(self):
        self.root = None
        print("Tree Deleted...\n")

    def show_person(self, search_name):
        person = self.search(search_name)
        if not person:
            print("Person not found.")
        else:
            gender = "Male" if person.gender else "Female"
            print(f"\nName: {person.name}")
            print(f"Age: {person.age}")
            print(f"Gender: {gender}")
            if person.child:
                print("Children: ", end="")
                child = person.child
                while child:
                    print(child.name, end=" ")
                    child = child.sibling
                print()
            else:
                print("No children.")
            if person.sibling:
                print("Siblings: ", end="")
                sibling = person.sibling
                while sibling:
                    print(sibling.name, end=" ")
                    sibling = sibling.sibling
                print()
            else:
                print("No siblings.")
            if person != self.root:
                parent = self.find_parent(self.root, person)
                if parent:
                    print(f"Parent: {parent.name}")
                else:
                    print("Parent not found.")
            else:
                print("No parent. Root node.")

    def find_parent(self, current, child):
        if not current:
            return None
        temp = current.child
        while temp:
            if temp == child:
                return current
            temp = temp.sibling
        sibling_result = self.find_parent(current.sibling, child)
        if sibling_result:
            return sibling_result
        return self.find_parent(current.child, child)

    def remove_person(self, name):
        if not self.root:
            print("Tree is empty.")
            return

        parent = self.find_parent(self.root, self.search(name))
        if parent:
            if parent.child and parent.child.name == name:
                parent.child = parent.child.sibling
            else:
                temp = parent.child
                while temp and temp.sibling and temp.sibling.name != name:
                    temp = temp.sibling
                if temp and temp.sibling:
                    temp.sibling = temp.sibling.sibling
        print("Person deleted successfully.")


def main():
    tree = FamilyTree()
    while True:
        print("\nFamily Tree Creator:")
        print("[1] Add Person")
        print("[2] Display Family Tree")
        print("[3] Search Person's details")
        print("[4] Delete Tree")
        print("[5] Delete Person")
        print("[0] Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Try again.")
            continue

        if choice == 1:
            tree.add_new_person()
        elif choice == 2:
            if tree.root:
                print("Family Tree:")
                tree.display_tree(tree.root)
            else:
                print("Family Tree is empty.")
        elif choice == 3:
            name = input("Enter the name of the person to show: ").strip()
            tree.show_person(name)
        elif choice == 4:
            tree.delete_tree()
        elif choice == 5:
            name = input("Enter the name of the person to delete: ").strip()
            tree.remove_person(name)
        elif choice == 0:
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
