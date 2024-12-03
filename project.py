class Person:
    def __init__(self, name="", age=0, gender=False):
        self.name = name
        self.age = age
        self.gender = gender 
        self.height = 0 
        self.child = None
        self.sibling = None

    def input_data(self):
        """Collects data for a person."""
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
            gender_input = input("Enter gender (m/f): ").strip().lower()
            if gender_input in ("m", "f"):
                self.gender = True if gender_input == "m" else False
                break
            else:
                print("Invalid input. Please enter 'm' or 'f'.")


class FamilyTree:
    def __init__(self):
        self.root = None 

    def add_person(self):
        """Adds a new person to the family tree."""
        new_person = Person()
        new_person.input_data()

        if not self.root:
            self.root = new_person
            print("Root person added successfully.\n")
            return

        related_name = input("\nEnter the name of the related person: ").strip()
        related_person = self.search(related_name)

        if not related_person:
            print(f"Person '{related_name}' not found. New person not added.\n")
            return

        print("Relationship Options:")
        print("[1] Add as Child")
        print("[2] Add as Sibling")
        while True:
            try:
                relationship = int(input("Enter relationship type (1/2): "))
                if relationship == 1:
                    self.add_child(related_person, new_person)
                elif relationship == 2:
                    self.add_sibling(related_person, new_person)
                else:
                    raise ValueError("Invalid choice. Enter 1 or 2.")
                break
            except ValueError as e:
                print(e)

        print(f"Person '{new_person.name}' added successfully.\n")

    def add_child(self, parent, child):
        """Adds a child to the specified parent."""
        if not parent.child:
            parent.child = child
        else:
            self.add_sibling(parent.child, child)
        child.height = parent.height + 1

    def add_sibling(self, sibling, new_sibling):
        """Adds a sibling to the specified sibling."""
        while sibling.sibling:
            sibling = sibling.sibling
        sibling.sibling = new_sibling
        new_sibling.height = sibling.height

    def search(self, name):
        """Searches for a person by name in the family tree."""
        return self._search_recursive(self.root, name)

    def _search_recursive(self, current, name):
        if not current:
            return None
        if current.name == name:
            return current
        return self._search_recursive(current.child, name) or self._search_recursive(current.sibling, name)

    def display_tree(self):
        """Displays the family tree."""
        if not self.root:
            print("Family Tree is empty.\n")
        else:
            print("Family Tree:")
            self._display_recursive(self.root)

    def _display_recursive(self, person, level=0):
        """Helper method to display the tree recursively."""
        if not person:
            return
        gender = "Male" if person.gender else "Female"
        print("  " * level + f"|-- {person.name} (Age: {person.age}, Gender: {gender})")
        self._display_recursive(person.child, level + 1)
        self._display_recursive(person.sibling, level)

    def delete_tree(self):
        """Deletes the entire family tree."""
        self.root = None
        print("Family tree deleted successfully.\n")

    def show_person(self, name):
        """Displays details of a specific person."""
        person = self.search(name)
        if not person:
            print(f"Person '{name}' not found.\n")
            return

        print(f"\nName: {person.name}")
        print(f"Age: {person.age}")
        print(f"Gender: {'Male' if person.gender else 'Female'}")

        
        if person.child:
            children = self._get_names(person.child)
            print(f"Children: {', '.join(children)}")
        else:
            print("No children.")

       
        siblings = self._get_names(person.sibling)
        if siblings:
            print(f"Siblings: {', '.join(siblings)}")
        else:
            print("No siblings.")

        
        parent = self._find_parent(self.root, person)
        if parent:
            print(f"Parent: {parent.name}")
        else:
            print("No parent (Root person).")

    def _get_names(self, person):
        """Helper to get all names from a linked list."""
        names = []
        while person:
            names.append(person.name)
            person = person.sibling
        return names

    def _find_parent(self, current, target):
        """Finds the parent of a specified person."""
        if not current:
            return None
        if current.child == target:
            return current
        for sibling in self._iterate_siblings(current.child):
            if sibling == target:
                return current
        return self._find_parent(current.child, target) or self._find_parent(current.sibling, target)

    def _iterate_siblings(self, person):
        """Iterates through siblings."""
        while person:
            yield person
            person = person.sibling

    def remove_person(self, name):
        """Removes a person by name from the tree."""
        if not self.root:
            print("Family tree is empty.\n")
            return

        if self.root.name == name:
            print("Cannot delete root person directly. Delete the tree instead.\n")
            return

        parent = self._find_parent(self.root, self.search(name))
        if not parent:
            print(f"Person '{name}' not found.\n")
            return

        
        if parent.child and parent.child.name == name:
            parent.child = parent.child.sibling
        else:
            prev_sibling = None
            for sibling in self._iterate_siblings(parent.child):
                if sibling.name == name:
                    if prev_sibling:
                        prev_sibling.sibling = sibling.sibling
                    break
                prev_sibling = sibling

        print(f"Person '{name}' removed successfully.\n")


def main():
    tree = FamilyTree()
    while True:
        print("\nFamily Tree Manager:")
        print("[1] Add Person")
        print("[2] Display Family Tree")
        print("[3] Show Person Details")
        print("[4] Delete Entire Tree")
        print("[5] Remove Person")
        print("[0] Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 5.\n")
            continue

        if choice == 1:
            tree.add_person()
        elif choice == 2:
            tree.display_tree()
        elif choice == 3:
            name = input("Enter name to search: ").strip()
            tree.show_person(name)
        elif choice == 4:
            tree.delete_tree()
        elif choice == 5:
            name = input("Enter name to remove: ").strip()
            tree.remove_person(name)
        elif choice == 0:
            print("Exiting Family Tree Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
