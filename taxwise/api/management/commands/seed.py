import pandas as pd
import tabula
from django.core.management.base import BaseCommand
from tabulate import tabulate
from taxwise.api.models import ChapterSection, Tarriff


class Command(BaseCommand):
    """
    This command will read tarriffs from the taffiff code and write them to the db.
    """

    help = "Generate tarriffs"

    PDF_FILE_NAME = "zimra-2022.pdf"
    PDF_PAGE_RANGE = "891-896"

    def _extract_statistical_unit_and_general_rate_of_duty(self, quantity):
        digits = [(i, c) for i, c in enumerate(str(quantity)) if c.isdigit()]
        if len(digits) > 1:
            general = str(quantity)[digits[1][0] :]
            unit = str(quantity)[: 1 * digits[1][0]]
            return unit, general
        else:
            return quantity, ""

    def _process_page_type_1(self, page_as_df):
        """
        Page with type conforming to the example below:

        Page number : 1 has 5 columns
        ['No.', 'Code', 'Unnamed: 0', 'data General', 'M.F.N.']
        +----+--------+------------+--------------------------------------------------+----------------+----------+
        |    |    No. | Code       | Unnamed: 0                                       | data General   | M.F.N.   |
        |----+--------+------------+--------------------------------------------------+----------------+----------|
        |  0 | nan    | nan        | - Other:                                         | nan            | nan      |
        |  1 | nan    | 0103.91.00 | - -Weighing less than 50 kg                      | 1. Kg10%       | 10%      |
        |  2 | nan    | nan        | nan                                              | 2.u            | nan      |
        |  3 | nan    | 0103.92.00 | - -Weighing 50 kg or more                        | 1. Kg10%       | 10%      |
        |  4 | nan    | nan        | nan                                              | 2.u            | nan      |
        |  5 |   1.04 | nan        | LIVE SHEEP AND GOATS.                            | nan            | nan      |
        """

        page_as_df.columns = ["Heading", "Commodity Code", "Description", "Quantity", "MFN"]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 1 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            print("****** data row ******")
            # print(data)
            print("type : " + str(type(row[1])))
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                # unit, general = self._extract_statistical_unit_and_general_rate_of_duty( quantity=str(data["Quantity"]))
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading=data["Heading"],
                commodity_code=data["Commodity Code"],
                description=data["Description"],
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_2(self, page_as_df):
        """
        Page with type conforming to the example below:

        Page number : 0 has 6 columns
        ['No.', 'Code', 'Unnamed: 0', 'data', 'General', 'M.F.N.']
        +----+-------+------------+---------------------------------+--------+-----------+----------+
        |    |   No. | Code       | Unnamed: 0                      | data   | General   | M.F.N.   |
        |----+-------+------------+---------------------------------+--------+-----------+----------|
        |  0 |   nan | 8541.30.00 | - Thyristors, diacs and triacs, | 1. Kg  | 5%        | 5%       |
        |  1 |   nan | nan        | other than photosensitive       | 2.u    | nan       | nan      |
        |  2 |   nan | nan        | devices                         | nan    | nan       | nan      |
        |  3 |   nan | nan        | - Photosensitive semiconductor  | nan    | nan       | nan      |
        |  4 |   nan | nan        | devices, including photovoltaic | nan    | nan       | nan      |

        --OR--
        +----+--------------+-----------------------------+--------------+---------+------+--------+
        |    | 8436.21.00   | - -Poultry incubators and   |   Unnamed: 0 | 1. Kg   | 0%   | 0%.1   |
        |----+--------------+-----------------------------+--------------+---------+------+--------|
        |  0 | nan          | brooders                    |          nan | 2.  u   | nan  | nan    |
        |  1 | 8436.29.00   | - -Other                    |          nan | 1. Kg   | 0%   | 0%     |
        |  2 | nan          | nan                         |          nan | 2.  u   | nan  | nan    |
        |  3 | 8436.80.00   | - Other machinery           |          nan | 1. Kg   | 0%   | 0%     |
        """
        
        if page_as_df.notnull()["Description"]:
            page_as_df.columns = ["Heading", "Commodity Code", "Description", "Quantity", "General", "MFN"]
        else:
            page_as_df.columns = ["Commodity Code", "Description", "Unamed", "Quantity", "General", "MFN"]

        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading=data.get("Heading") or "",
                commodity_code=data["Commodity Code"],
                description=data["Description"],
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_3(self, page_as_df):
        """
        Page with type conforming to the example below:

        """
        page_as_df.columns = ["Heading", "Commodity Code", "Description", "Unamed", "Quantity", "General", "MFN"]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading=data["Heading"],
                commodity_code=data["Commodity Code"],
                description=data["Description"],
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_4(self, page_as_df):
        """
        Page with type conforming to the example below:

        Page number : 135 has 8 columns
        ['No.', 'Code', 'Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'data', 'General', 'M.F.N.']
        +----+-------+------------+-----------------------------------------------------+--------------------+--------------+--------+-----------+----------+
        |    |   No. | Code       | Unnamed: 0                                          | Unnamed: 1         | Unnamed: 2   | data   | General   | M.F.N.   |
        |----+-------+------------+-----------------------------------------------------+--------------------+--------------+--------+-----------+----------|
        |  0 |   nan | 2009.39.00 | - -Other                                            | nan                | nan          | Kg     | 40%       | 40%      |
        |  1 |   nan | nan        | - Pineapple juice :                                 | nan                | nan          | nan    | nan       | nan      |
        |  2 |   nan | 2009.41.00 | - -Of a Brix value not                              | nan                | nan          | Kg     | 40%       | 40%      |
        |  3 |   nan | nan        | exceeding 20                                        | nan                | nan          | nan    | nan       | nan      |
        |  4 |   nan | 2009.49.00 | - -Other                                            | nan                | nan          | K  g   | 4  0  %   | 40%      |
        |  5 |   nan | nan        | nan                                                 | nan                | nan          | nan    | nan       | nan      |
        |  6 |   nan | 2009.50.00 | - Tomato juice                                      | nan                | nan          | Kg     | 40%       | 40%      |
        """
        page_as_df.columns = [
            "Heading",
            "Commodity Code",
            "Description",
            "Unamed",
            "Unamed",
            "Quantity",
            "General",
            "MFN",
        ]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading=data["Heading"],
                commodity_code=data["Commodity Code"],
                description=data["Description"],
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_5(self, page_as_df):
        """
        Page with type conforming to the example below:

        Page number : 94 has 3 columns
        ['2.1000u', 'US$5.00/', 'US$5.00/.1']
        +----+-----------+--------------+--------------+
        |    |   2.1000u | US$5.00/     | US$5.00/.1   |
        |----+-----------+--------------+--------------|
        |  0 |       nan | 1000         | 1000         |
        |  1 |       nan | cigarettes + | cigarettes + |
        |  2 |       nan | Excise       | Excise       |
        +----+-----------+--------------+--------------+                                    | nan                | nan          | Kg     | 40%       | 40%      |
        """
        page_as_df.columns = ["Quantity", "General", "MFN"]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading="",
                commodity_code="",
                description="",
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_6(self, page_as_df):
        """
        Page with type conforming to the example below:

        Page number : 95 has 4 columns
        ['cigarillos not containing', '2.1000u', 'US$5.00/', 'US$5.00/.1']
        +----+-----------------------------+-----------+--------------+--------------+
        |    | cigarillos not containing   |   2.1000u | US$5.00/     | US$5.00/.1   |
        |----+-----------------------------+-----------+--------------+--------------|
        |  0 | tobacco                     |       nan | 1000         | 1000         |
        |  1 | nan                         |       nan | cigarettes + | cigarettes + |
        |  2 | nan                         |       nan | Excise       | Excise       |
        +----+-----------------------------+-----------+--------------+--------------+                                   | nan                | nan          | Kg     | 40%       | 40%      |
        """
        page_as_df.columns = ["Description", "Quantity", "General", "MFN"]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading="",
                commodity_code="",
                description=data["Description"],
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_8(self, page_as_df):
        """
        Page with type conforming to the example below:

        ['5  5  1  6  . 1  3  . 1  0', '-  --', 'C', 'a n  v  a  s', 'w  e  i g  h  i n g not', 'Unnamed: 0', '1. Kg', '10%', '10%.1']
        +----+------------------------------+--------------------------------+---------------------+----------------+---------------------------+--------------+---------+-------+---------+
        |    | 5  5  1  6  . 1  3  . 1  0   | -  --                          | C                   | a n  v  a  s   | w  e  i g  h  i n g not   |   Unnamed: 0 | 1. Kg   | 10%   | 10%.1   |
        |----+------------------------------+--------------------------------+---------------------+----------------+---------------------------+--------------+---------+-------+---------|
        |  0 | nan                          | nan                            | nan                 | nan            | 2                         |          nan | 2       | nan   | nan     |
        |  1 | nan                          | less than 340 g/m              | nan                 | nan            | nan                       |          nan | 2.  m   | nan   | nan     |
        |  2 | 5516.13.90                   | - - -                          | Other               | nan            | nan                       |          nan | 1. Kg   | 10%   | 10%     |
        |  3 | nan                          | nan                            | nan                 | nan            | nan                       |          nan | 2       | nan   | nan     |
        |  4 | nan                          | nan                            | nan                 | nan            | nan                       |          nan | 2.  m   | nan   | nan     |
        |  5 | nan                          | - - Printed :                  | nan                 | nan            | nan                       |          nan | nan     | nan   | nan     |
        |  6 | 5  5  1  6  . 1  4  . 1  0   | -  --                          | C                   | a n  v  a  s   | w  e  i g  h  i n g not   |          nan | 1. Kg   | 10%   | 10%     |
        |  7 | nan                          | nan                            | nan                 | nan            | 2                         |          nan | 2       | nan   | nan     |
        |  8 | nan                          | less than 340 g/m              | nan                 | nan            | nan                       |          nan | 2.  m   | nan   | nan     |
        |  9 | nan                          | nan                            | nan                 | nan            | nan                       |          nan | nan     | nan   | nan     |

        """
        page_as_df.columns = [
            "Commodity Code",
            "Description",
            "Unamed_1",
            "Unamed_2",
            "Unamed_3",
            "Unamed_4",
            "Quantity",
            "General",
            "MFN",
        ]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading="",
                commodity_code=data["Commodity Code"],
                description=str(data["Description"])
                + " "
                + str(data["Unamed_1"])
                + " "
                + str(data["Unamed_2"])
                + " "
                + str(data["Unamed_3"])
                + " "
                + str(data["Unamed_4"]),
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_section_header_row(self, row: pd.Series):
        """
        Process Type 3 type
        """

        if row.get("Heading") and row.Heading != "Heading" and str(row.Heading) != "nan":
            print("****** section row ******")
            print(row)
            chapter_section = ChapterSection(
                chapter=str(row.get("Heading")).split(".")[0],
                section=row.get("Heading"),
                description=row.get("Description"),
            )
            chapter_section.save()

    def _write_axes(self, df):
        """
        Write Axes
        """
        # write axes
        # ['0104.10.10', '- - -Pure-bred breeding sheep', '1. Kg', '0%', '0%.1']
        if len(df.columns) == 4:
            print(df.axes[1].tolist())
            tarriff = Tarriff(
                heading=df.axes[1].tolist()[0],
                commodity_code=df.axes[1].tolist()[1],
                description=df.axes[1].tolist()[2],
                statistical_unit=df.axes[1].tolist()[3],
                general_rate_of_duty=df.axes[1].tolist()[3],
                # mtf_rate_of_duty=data[5],
            )
            tarriff.save()

    def _get_page_type(self, number_of_columns: int):

        if number_of_columns == 5:
            return "type_1"
        elif number_of_columns == 6:
            return "type_2"
        elif number_of_columns == 7:
            return "type_3"
        elif number_of_columns == 8:
            return "type_4"
        elif number_of_columns == 3:
            return "type_5"
        elif number_of_columns == 4:
            return "type_6"
        elif number_of_columns == 2:
            return "type_7"
        elif number_of_columns == 9:
            return "type_8"

        else:
            raise ValueError(f"Unknown type with: {number_of_columns} columns")

    def process_page_data(self, page_as_df):
        """
        Process the page
        """
        try:
            page_type = self._get_page_type(number_of_columns=len(page_as_df.columns))
        except ValueError:
            print("**** Unhandled page type *** ")
            print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
            raise

        if page_type == "type_1":
            self._process_page_type_1(page_as_df)
        elif page_type == "type_2":
            self._process_page_type_2(page_as_df)
        elif page_type == "type_3":
            self._process_page_type_3(page_as_df)
        elif page_type == "type_4":
            self._process_page_type_4(page_as_df)
        elif page_type == "type_5":
            self._process_page_type_5(page_as_df)
        elif page_type == "type_6":
            self._process_page_type_6(page_as_df)

        elif page_type == "type_7":
            return
        elif page_type == "type_8":
            self._process_page_type_8(page_as_df)

    def generate_tarriffs(self):
        try:
            list_of_df = tabula.read_pdf(self.PDF_FILE_NAME, pages=self.PDF_PAGE_RANGE)
            tabula.convert_into(
                self.PDF_FILE_NAME, "test.csv", output_format="csv", stream=True, pages=self.PDF_PAGE_RANGE
            )

            # print(list_of_df)
        except Exception as e:
            print(f"An error occurred while reading the pdf file: {e}")
            return

        for idx, page_df in enumerate(list_of_df):
            if isinstance(page_df, pd.DataFrame):
                print("---------------------------------")
                print(f"Page number : {idx} has {len(page_df.columns)} columns")
                print(page_df.axes[1].tolist())
                print(tabulate(page_df, headers="keys", tablefmt="psql"))
                print("---------------------------------")
                self.process_page_data(page_df)

    def handle(self, *args, **options):
        self.stdout.write("Seeding tarriffs...")
        self.generate_tarriffs()
        self.stdout.write("\n\nTarriffs saved !!!")

    def _process_page_type_4(self, page_as_df):
        """
        Page with type conforming to the example below:

        Page number : 135 has 8 columns
        ['No.', 'Code', 'Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2', 'data', 'General', 'M.F.N.']
        +----+-------+------------+-----------------------------------------------------+--------------------+--------------+--------+-----------+----------+
        |    |   No. | Code       | Unnamed: 0                                          | Unnamed: 1         | Unnamed: 2   | data   | General   | M.F.N.   |
        |----+-------+------------+-----------------------------------------------------+--------------------+--------------+--------+-----------+----------|
        |  0 |   nan | 2009.39.00 | - -Other                                            | nan                | nan          | Kg     | 40%       | 40%      |
        |  1 |   nan | nan        | - Pineapple juice :                                 | nan                | nan          | nan    | nan       | nan      |
        |  2 |   nan | 2009.41.00 | - -Of a Brix value not                              | nan                | nan          | Kg     | 40%       | 40%      |
        |  3 |   nan | nan        | exceeding 20                                        | nan                | nan          | nan    | nan       | nan      |
        |  4 |   nan | 2009.49.00 | - -Other                                            | nan                | nan          | K  g   | 4  0  %   | 40%      |
        |  5 |   nan | nan        | nan                                                 | nan                | nan          | nan    | nan       | nan      |
        |  6 |   nan | 2009.50.00 | - Tomato juice                                      | nan                | nan          | Kg     | 40%       | 40%      |
        """
        page_as_df.columns = [
            "Heading",
            "Commodity Code",
            "Description",
            "Unamed",
            "Unamed",
            "Quantity",
            "General",
            "MFN",
        ]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading=data["Heading"],
                commodity_code=data["Commodity Code"],
                description=data["Description"],
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_5(self, page_as_df):
        """
        Page with type conforming to the example below:

        Page number : 94 has 3 columns
        ['2.1000u', 'US$5.00/', 'US$5.00/.1']
        +----+-----------+--------------+--------------+
        |    |   2.1000u | US$5.00/     | US$5.00/.1   |
        |----+-----------+--------------+--------------|
        |  0 |       nan | 1000         | 1000         |
        |  1 |       nan | cigarettes + | cigarettes + |
        |  2 |       nan | Excise       | Excise       |
        +----+-----------+--------------+--------------+                                    | nan                | nan          | Kg     | 40%       | 40%      |
        """
        page_as_df.columns = ["Quantity", "General", "MFN"]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading="",
                commodity_code="",
                description="",
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_6(self, page_as_df):
        """
        Page with type conforming to the example below:

        Page number : 95 has 4 columns
        ['cigarillos not containing', '2.1000u', 'US$5.00/', 'US$5.00/.1']
        +----+-----------------------------+-----------+--------------+--------------+
        |    | cigarillos not containing   |   2.1000u | US$5.00/     | US$5.00/.1   |
        |----+-----------------------------+-----------+--------------+--------------|
        |  0 | tobacco                     |       nan | 1000         | 1000         |
        |  1 | nan                         |       nan | cigarettes + | cigarettes + |
        |  2 | nan                         |       nan | Excise       | Excise       |
        +----+-----------------------------+-----------+--------------+--------------+                                   | nan                | nan          | Kg     | 40%       | 40%      |
        """
        page_as_df.columns = ["Description", "Quantity", "General", "MFN"]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading="",
                commodity_code="",
                description=data["Description"],
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_page_type_8(self, page_as_df):
        """
        Page with type conforming to the example below:

        ['5  5  1  6  . 1  3  . 1  0', '-  --', 'C', 'a n  v  a  s', 'w  e  i g  h  i n g not', 'Unnamed: 0', '1. Kg', '10%', '10%.1']
        +----+------------------------------+--------------------------------+---------------------+----------------+---------------------------+--------------+---------+-------+---------+
        |    | 5  5  1  6  . 1  3  . 1  0   | -  --                          | C                   | a n  v  a  s   | w  e  i g  h  i n g not   |   Unnamed: 0 | 1. Kg   | 10%   | 10%.1   |
        |----+------------------------------+--------------------------------+---------------------+----------------+---------------------------+--------------+---------+-------+---------|
        |  0 | nan                          | nan                            | nan                 | nan            | 2                         |          nan | 2       | nan   | nan     |
        |  1 | nan                          | less than 340 g/m              | nan                 | nan            | nan                       |          nan | 2.  m   | nan   | nan     |
        |  2 | 5516.13.90                   | - - -                          | Other               | nan            | nan                       |          nan | 1. Kg   | 10%   | 10%     |
        |  3 | nan                          | nan                            | nan                 | nan            | nan                       |          nan | 2       | nan   | nan     |
        |  4 | nan                          | nan                            | nan                 | nan            | nan                       |          nan | 2.  m   | nan   | nan     |
        |  5 | nan                          | - - Printed :                  | nan                 | nan            | nan                       |          nan | nan     | nan   | nan     |
        |  6 | 5  5  1  6  . 1  4  . 1  0   | -  --                          | C                   | a n  v  a  s   | w  e  i g  h  i n g not   |          nan | 1. Kg   | 10%   | 10%     |
        |  7 | nan                          | nan                            | nan                 | nan            | 2                         |          nan | 2       | nan   | nan     |
        |  8 | nan                          | less than 340 g/m              | nan                 | nan            | nan                       |          nan | 2.  m   | nan   | nan     |
        |  9 | nan                          | nan                            | nan                 | nan            | nan                       |          nan | nan     | nan   | nan     |

        """
        page_as_df.columns = [
            "Commodity Code",
            "Description",
            "Unamed_1",
            "Unamed_2",
            "Unamed_3",
            "Unamed_4",
            "Quantity",
            "General",
            "MFN",
        ]
        print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
        print("**********************")

        for row in page_as_df.iterrows():
            data = row[1].fillna("")

            print("****** data row : type 2 ******")
            print("type : " + str(type(row[1])))
            print(row)
            print("**********************")

            general = ""
            unit = ""
            if data.notnull()["Quantity"]:
                print("qty : " + str(data["Quantity"]))
                digits = [(i, c) for i, c in enumerate(str(data["Quantity"])) if c.isdigit()]
                print("-- digits :" + str(digits))

                if len(digits) > 1:
                    general = str(data["Quantity"])[digits[1][0] :]
                    unit = str(data["Quantity"])[: 1 * digits[1][0]]

            tarriff = Tarriff(
                heading="",
                commodity_code=data["Commodity Code"],
                description=str(data["Description"])
                + " "
                + str(data["Unamed_1"])
                + " "
                + str(data["Unamed_2"])
                + " "
                + str(data["Unamed_3"])
                + " "
                + str(data["Unamed_4"]),
                statistical_unit=unit or data["Quantity"],
                general_rate_of_duty=data["General"] or general,
                mtf_rate_of_duty=data["MFN"],
            )
            tarriff.save()

    def _process_section_header_row(self, row: pd.Series):
        """
        Process Type 3 type
        """

        if row.get("Heading") and row.Heading != "Heading" and str(row.Heading) != "nan":
            print("****** section row ******")
            print(row)
            chapter_section = ChapterSection(
                chapter=str(row.get("Heading")).split(".")[0],
                section=row.get("Heading"),
                description=row.get("Description"),
            )
            chapter_section.save()

    def _write_axes(self, df):
        """
        Write Axes
        """
        # write axes
        # ['0104.10.10', '- - -Pure-bred breeding sheep', '1. Kg', '0%', '0%.1']
        if len(df.columns) == 4:
            print(df.axes[1].tolist())
            tarriff = Tarriff(
                heading=df.axes[1].tolist()[0],
                commodity_code=df.axes[1].tolist()[1],
                description=df.axes[1].tolist()[2],
                statistical_unit=df.axes[1].tolist()[3],
                general_rate_of_duty=df.axes[1].tolist()[3],
                # mtf_rate_of_duty=data[5],
            )
            tarriff.save()

    def _get_page_type(self, number_of_columns: int):

        if number_of_columns == 5:
            return "type_1"
        elif number_of_columns == 6:
            return "type_2"
        elif number_of_columns == 7:
            return "type_3"
        elif number_of_columns == 8:
            return "type_4"
        elif number_of_columns == 3:
            return "type_5"
        elif number_of_columns == 4:
            return "type_6"
        elif number_of_columns == 2:
            return "type_7"
        elif number_of_columns == 9:
            return "type_8"

        else:
            raise ValueError(f"Unknown type with: {number_of_columns} columns")

    def process_page_data(self, page_as_df):
        """
        Process the page
        """
        try:
            page_type = self._get_page_type(number_of_columns=len(page_as_df.columns))
        except ValueError:
            print("**** Unhandled page type *** ")
            print(tabulate(page_as_df, headers="keys", tablefmt="psql"))
            raise

        if page_type == "type_1":
            self._process_page_type_1(page_as_df)
        elif page_type == "type_2":
            self._process_page_type_2(page_as_df)
        elif page_type == "type_3":
            self._process_page_type_3(page_as_df)
        elif page_type == "type_4":
            self._process_page_type_4(page_as_df)
        elif page_type == "type_5":
            self._process_page_type_5(page_as_df)
        elif page_type == "type_6":
            self._process_page_type_6(page_as_df)

        elif page_type == "type_7":
            return
        elif page_type == "type_8":
            self._process_page_type_8(page_as_df)

    def generate_tarriffs(self):
        try:
            list_of_df = tabula.read_pdf(self.PDF_FILE_NAME, pages=self.PDF_PAGE_RANGE)
            tabula.convert_into(
                self.PDF_FILE_NAME, "test.csv", output_format="csv", stream=True, pages=self.PDF_PAGE_RANGE
            )

            # print(list_of_df)
        except Exception as e:
            print(f"An error occurred while reading the pdf file: {e}")
            return

        for idx, page_df in enumerate(list_of_df):
            if isinstance(page_df, pd.DataFrame):
                print("---------------------------------")
                print(f"Page number : {idx} has {len(page_df.columns)} columns")
                print(page_df.axes[1].tolist())
                print(tabulate(page_df, headers="keys", tablefmt="psql"))
                print("---------------------------------")
                self.process_page_data(page_df)

    def handle(self, *args, **options):
        self.stdout.write("Seeding tarriffs...")
        self.generate_tarriffs()
        self.stdout.write("\n\nTarriffs saved !!!")
