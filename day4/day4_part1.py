# --- Day 4: Passport Processing ---
# You arrive at the airport only to realize that you grabbed your
# North Pole Credentials instead of your passport. While these
# documents are extremely similar, North Pole Credentials aren't
# issued by a country and therefore aren't actually valid
# documentation for travel in most of the world.
#
# It seems like you're not the only one having problems, though; a very long
# line has formed for the automatic passport scanners, and the delay could
# upset your travel itinerary.
#
# Due to some questionable network security, you realize you might be able to
# solve both of these problems at the same time.
#
# The automatic passport scanners are slow because they're having trouble
# detecting which passports have all required fields. The expected fields
# are as follows:
#
# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)
# Passport data is validated in batch files (your puzzle input). Each passport
# is represented as a sequence of key:value pairs separated by spaces or
# newlines. Passports are separated by blank lines.
#
# Here is an example batch file containing four passports:
#
# ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
# byr:1937 iyr:2017 cid:147 hgt:183cm
#
# iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
# hcl:#cfa07d byr:1929
#
# hcl:#ae17e1 iyr:2013
# eyr:2024
# ecl:brn pid:760753108 byr:1931
# hgt:179cm
#
# hcl:#cfa07d eyr:2025 pid:166559648
# iyr:2011 ecl:brn hgt:59in
# The first passport is valid - all eight fields are present. The second
# passport is invalid - it is missing hgt (the Height field).
#
# The third passport is interesting; the only missing field is cid, so it
# looks like data from North Pole Credentials, not a passport at all!
# Surely, nobody would mind if you made the system temporarily ignore
# missing cid fields. Treat this "passport" as valid.
#
# The fourth passport is missing two fields, cid and byr. Missing cid is fine,
# but missing any other field is not, so this passport is invalid.
#
# According to the above rules, your improved system would report 2
# valid passports.
#
# Count the number of valid passports - those that have all required fields.
# Treat cid as optional. In your batch file, how many passports are valid?


class Passport:
    def __init__(self):
        self.fields = {}

    def __repr__(self):
        s = ""
        sep = ""
        for k, v in self.fields.items():
            s += sep
            s += f"{k}:{v}"
            sep = ", "
        return s

    def add_field(self, field_name: str, field_value: str):
        """
        Add a field to this passport
        """
        # for now, going to throw on duplicate fields, invalid field names will be accepted though
        if field_name in self.fields:
            raise ValueError("This passport already contains a field {field_name}")
        self.fields[field_name] = field_value

    def is_valid(self) -> bool:
        """
        Determine if the passport has the required fields to be considered valid
        """
        required_fields = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
        result = True
        for this_fieldname in required_fields:
            if this_fieldname not in self.fields:
                result = False
        return result


def load_passports_from_file(filename: str):
    """
    Returns a list of passports based on the input file passed.
    Each passport is blank-line separated
    non-blank lines have 1 or more whitespace separated field:val pairs
    """
    all_passports = []

    # currently we're not working on a passport
    this_passport = None

    # loop through everything in the file
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            # ok, if the line is blank then we need to store any current passport that we're working on and then clean up
            if "" == this_line:
                if this_passport is not None:
                    all_passports.append(this_passport)
                this_passport = None
            else:
                # if we're not working on a passport then we need to create a new one
                if this_passport is None:
                    this_passport = Passport()

                # ok, this has one or more space-delimeted key/value pairs
                field_pairs = this_line.split()

                # process each pair
                for this_pair in field_pairs:
                    field_name, field_value = this_pair.split(":", 1)
                    this_passport.add_field(field_name, field_value)

    # and we might have a passport that we've not finished
    if this_passport is not None:
        all_passports.append(this_passport)

    return all_passports


filename = "input.txt"

passports = load_passports_from_file(filename)

valid_count = 0
for this_passport in passports:
    print(f"{this_passport} -> {this_passport.is_valid()}")
    if this_passport.is_valid():
        valid_count += 1

print(f"Total valid passports: {valid_count}")
