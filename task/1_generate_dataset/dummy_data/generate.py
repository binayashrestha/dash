import csv
import random
from datetime import timedelta
from faker import Faker
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EmployeeLeaveRecordGenerator:
    def __init__(self, num_records):
        self.fake = Faker()
        self.num_records = num_records

    def generate(self):
        """Generate a list of employee leave records."""
        return [self._generate_leave_record() for _ in range(self.num_records)]

    def save_to_csv(self, records, filename='employee_leave_records.csv'):
        """Save generated records to a CSV file."""
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
            logging.info(f"Generated {len(records)} records in '{filename}'.")
        except Exception as e:
            logging.error(f"Failed to write to file {filename}: {e}")

    def _generate_leave_record(self):
        """Private method to generate a single leave record with detailed data."""
        start_date, end_date = self._random_date_pair()
        return {
            'Employee ID': self.fake.unique.uuid4(),
            'Name': self.fake.name(),
            'Age': random.randint(18, 65),
            'Gender': self._random_gender(),
            'Department': self._random_department(),
            'Position': self.fake.job(),
            'Manager': self.fake.name(),
            'Contact Information': self.fake.phone_number(),
            'Emergency Contact': self.fake.phone_number(),
            'Leave Type': self._random_leave_type(),
            'Reason for Leave': self._generate_reason_for_leave(),
            'Leave Start Date': start_date,
            'Leave End Date': end_date,
            'Return to Work Date': end_date + timedelta(days=1),
            'Duration': (end_date - start_date).days,
            'Leave Request Date': start_date - timedelta(days=random.randint(1, 10)),
            'Approval Status': self._random_approval_status(),
            'Leave Approval Date': start_date - timedelta(days=random.randint(0, 5)),
            'Notification Method': self._random_notification_method(),
            'Substitute/Backup Employee': self.fake.name(),
            'Training Required': random.choice([True, False]),
            'Previous Leave History': self._generate_previous_leave_history(),
            'Leave Balance': random.randint(0, 30),
            'Annual Leave Quota': random.randint(10, 30),
            'Remote Work Option': random.choice([True, False]),
            'Health Status': 'Good',
            'Comments from HR': self._generate_comments_from_hr(),
            'Document Attachment': self._generate_document_attachment(),
            'Cost Center': self.fake.company()
        }

    def _random_gender(self):
        return random.choice(['Male', 'Female', 'Other'])

    def _random_department(self):
        return random.choice(['HR', 'IT', 'Sales', 'Marketing', 'Operations'])

    def _random_leave_type(self):
        return random.choice(['Annual', 'Sick', 'Maternity', 'Paternity'])

    def _random_approval_status(self):
        return random.choice(['Approved', 'Denied'])

    def _random_notification_method(self):
        return random.choice(['Email', 'Phone call'])

    def _random_date_pair(self):
        start_date = self.fake.date_between(start_date='-1y', end_date='today')
        end_date = start_date + timedelta(days=random.randint(1, 30))
        return start_date, end_date

    def _generate_reason_for_leave(self):
        reasons = ['Medical treatment', 'Vacation travel', 'Family obligation', 'Educational course']
        return random.choice(reasons)

    def _generate_previous_leave_history(self):
        number_of_leaves = random.randint(0, 5)
        return f"{number_of_leaves} leaves in the past year"

    def _generate_comments_from_hr(self):
        comments = ['Reviewed', 'Requires follow-up', 'No issues', 'Please update contact details']
        return random.choice(comments) if random.random() < 0.5 else 'No comments'

    def _generate_document_attachment(self):
        """Generates a dummy file name for a document attachment."""
        try:
            # Using default category as Faker does not have 'document' as a built-in category.
            if random.random() < 0.3:
                return f"{self.fake.file_name()}"
            return 'None'
        except KeyError as e:
            logging.error(f"Failed to generate file name: {e}")
            return 'None'


# Example usage
if __name__ == '__main__':
    generator = EmployeeLeaveRecordGenerator(num_records=10000)
    records = generator.generate()
    generator.save_to_csv(records)
