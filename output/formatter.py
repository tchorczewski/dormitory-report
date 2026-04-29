class Formatter:
    def __init__(self, data, extension):
        self.data = data
        self.extension = extension
        self.file_path = f"results/report.{extension}"

    def export(self):
        '''Exports the report data in the specified format (JSON/XML) and saves it to a file in the results directory.'''
        if self.extension == 'json':
            return self._format_json()
        elif self.extension == 'xml':
            return self._format_xml()
        else:
            raise ValueError(f"Unsupported format: {self.extension}")

    def _format_json(self):
        '''Formats the report data as JSON and saves it to a file'''
        import json
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error occurred while formatting JSON: {e}")

    def _format_xml(self):
        '''Formats the report data as XML and saves it to a file'''
        import xml.etree.ElementTree as ET
        root = ET.Element("results")
        for section_name, rows in self.data.items():
            item_elem = ET.SubElement(root,section_name)
            for row in rows:
                child = ET.SubElement(item_elem, "record")
                for key, value in row.items():
                    item_child = ET.SubElement(child, key)
                    item_child.text = str(value)
        ET.indent(root)
        try:
            tree = ET.ElementTree(root)
            tree.write(self.file_path, encoding='utf-8', xml_declaration=True)
        except Exception as e:
            print(f"Error occurred while formatting XML: {e}")
        return None
    