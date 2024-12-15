import csv

class Person:
    def __init__(self, name="", age=0, gender=False):
        self.name = name
        self.age = age
        self.gender = gender
        self.child = None
        self.sibling = None

    def input_data(self):
        try:
            self.name = input("Enter name: ").strip()
            self.age = int(input("Enter age: "))
            if self.age <= 0:
                raise ValueError("Age must be a positive number.")
            gender_input = input("Enter gender (m/f): ").strip().lower()
            if gender_input not in ("m", "f"):
                raise ValueError("Invalid gender. Please enter 'm' or 'f'.")
            self.gender = gender_input == "m"
        except Exception as e:
            print(f"Input error: {e}")
            raise

class FamilyTree:
    def __init__(self, csv_file="family_tree.csv"):
        self.root = None
        self.csv_file = csv_file
        self.load_from_csv()

    def save_to_csv(self):
        """Saves the current family tree to the CSV file."""
        with open(self.csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Age", "Gender", "Parent", "Sibling"])
            self._write_to_csv(self.root, None, writer)

    def _write_to_csv(self, person, parent_name, writer):
        if not person:
            return
        gender = "m" if person.gender else "f"
        sibling_name = person.sibling.name if person.sibling else None
        writer.writerow([person.name, person.age, gender, parent_name, sibling_name])
        self._write_to_csv(person.child, person.name, writer)
        self._write_to_csv(person.sibling, parent_name, writer)

    def load_from_csv(self):
        """Loads the family tree from the CSV file."""
        try:
            with open(self.csv_file, "r") as file:
                reader = csv.DictReader(file)
                nodes = {}

                for row in reader:
                    name = row["Name"]
                    age = int(row["Age"])
                    gender = row["Gender"] == "m"
                    parent = row["Parent"]
                    sibling = row["Sibling"]

                    person = nodes.get(name, Person(name, age, gender))
                    person.age = age
                    person.gender = gender
                    nodes[name] = person

                    if parent:
                        parent_node = nodes.get(parent)
                        if not parent_node:
                            parent_node = Person(parent)
                            nodes[parent] = parent_node
                        if not parent_node.child:
                            parent_node.child = person
                        else:
                            self.add_sibling(parent_node.child, person)

                    if sibling:
                        sibling_node = nodes.get(sibling)
                        if not sibling_node:
                            sibling_node = Person(sibling)
                            nodes[sibling] = sibling_node
                        person.sibling = sibling_node

                self.root = nodes.get(next(iter(nodes)) if nodes else None)
        except FileNotFoundError:
            print(f"CSV file '{self.csv_file}' not found. Starting with an empty family tree.")

    def add_person(self):
        try:
            new_person = Person()
            new_person.input_data()

            if not self.root:
                self.root = new_person
                print("Root person added successfully.\n")
                self.save_to_csv()
                return

            related_name = input("\nEnter the name of the related person: ").strip()
            related_person = self.search(related_name)

            if not related_person:
                print(f"Person '{related_name}' not found. New person not added.\n")
                return

            print("Relationship Options:")
            print("[1] Add as Child")
            print("[2] Add as Sibling")
            choice = int(input("Enter relationship type (1/2): "))
            if choice == 1:
                self.add_child(related_person, new_person)
            elif choice == 2:
                self.add_sibling(related_person, new_person)
            else:
                raise ValueError("Invalid choice. Enter 1 or 2.")

            print(f"Person '{new_person.name}' added successfully.\n")
            self.save_to_csv()
        except Exception as e:
            print(f"Error adding person: {e}")

    def add_child(self, parent, child):
        if not parent.child:
            parent.child = child
        else:
            self.add_sibling(parent.child, child)

    def add_sibling(self, sibling, new_sibling):
        while sibling.sibling:
            sibling = sibling.sibling
        sibling.sibling = new_sibling

    def search(self, name):
        return self._search_recursive(self.root, name)

    def _search_recursive(self, current, name):
        if not current:
            return None
        if current.name == name:
            return current
        return self._search_recursive(current.child, name) or self._search_recursive(current.sibling, name)

    def display_tree(self):
        if not self.root:
            print("Family Tree is empty.\n")
        else:
            print("Family Tree:")
            self._display_recursive(self.root)

    def _display_recursive(self, person, level=0):
        if not person:
            return
        gender = "Male" if person.gender else "Female"
        print("  " * level + f"|-- {person.name} (Age: {person.age}, Gender: {gender})")
        self._display_recursive(person.child, level + 1)
        self._display_recursive(person.sibling, level)

    def remove_person(self, name):
        try:
            if not self.root:
                print("Family tree is empty.\n")
                return

            if self.root.name == name:
                if self.root.child:
                    print("Cannot remove root with children. Assign a new root first.")
                    return
                self.root = self.root.sibling
                print(f"Root person '{name}' removed successfully.\n")
                self.save_to_csv()
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
            self.save_to_csv()
        except Exception as e:
            print(f"Error removing person: {e}")

    def delete_tree(self):
        self.root = None
        self.save_to_csv()
        print("Family tree deleted successfully.\n")

    def show_person(self, name):
        try:
            person = self.search(name)
            if not person:
                print(f"Person '{name}' not found.\n")
                return

            print(f"\nName: {person.name}")
            print(f"Age: {person.age}")
            print(f"Gender: {'Male' if person.gender else 'Female'}")

            parent = self._find_parent(self.root, person)
            siblings = self._get_names(parent.child if parent else self.root, exclude=person.name)
            print(f"Siblings: {', '.join(siblings) if siblings else 'No siblings.'}")

            children = self._get_names(person.child)
            print(f"Children: {', '.join(children) if children else 'No children.'}")

            print(f"Parent: {parent.name if parent else 'No parent (Root person).'}")
        except Exception as e:
            print(f"Error showing person details: {e}")

    def _get_names(self, person, exclude=None):
        names = []
        while person:
            if person.name != exclude:
                names.append(person.name)
            person = person.sibling
        return names

    def _find_parent(self, current, target):
        if not current or not target:
            return None
        if current.child == target:
            return current
        for sibling in self._iterate_siblings(current.child):
            if sibling == target:
                return current
        return self._find_parent(current.child, target) or self._find_parent(current.sibling, target)

    def _iterate_siblings(self, person):
        while person:
            yield person
            person = person.sibling

    def _display_recursive(self, person, level=0):
        if not person:
            return
        gender = "Male" if person.gender else "Female"
        print("  " * level + f"|-- {person.name} (Age: {person.age}, Gender: {gender})")
        self._display_recursive(person.child, level + 1)
        self._display_recursive(person.sibling, level)

# Main program
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
            choice = input("Enter your choice: ").strip()
            if not choice.isdigit():
                raise ValueError("Choice must be a number.")

            choice = int(choice)
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
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
