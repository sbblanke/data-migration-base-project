"""
Email Message Data Generator
Simulates Salesforce EmailMessage object data for migration testing
"""

import pandas as pd
from faker import Faker
import uuid
from datetime import datetime, timedelta
import random

fake = Faker()

class EmailMessageGenerator:
    def __init__(self, seed=42):
        """Initialize with seed for reproducible data"""
        Faker.seed(seed)
        random.seed(seed)
        
    def generate_email_batch(self, num_emails=1000):
        """Generate a batch of mock EmailMessage records"""
        
        print(f"Generating {num_emails} mock email records...")
        
        emails = []
        
        # Common email patterns for realistic data
        email_types = ['customer_inquiry', 'support_ticket', 'sales_follow_up', 'internal', 'newsletter']
        priorities = ['Low', 'Normal', 'High']
        statuses = ['Sent', 'Draft', 'Failed', 'Bounced']
        
        for i in range(num_emails):
            email_type = random.choice(email_types)
            
            # Generate realistic email content based on type
            subject, body = self._generate_content_by_type(email_type)
            
            email_record = {
                'Id': f'02s{fake.random_number(digits=15)}',  # Salesforce EmailMessage ID format
                'Subject': subject,
                'TextBody': body,
                'HtmlBody': f'<html><body>{body}</body></html>',
                'FromAddress': fake.email(),
                'ToAddress': fake.email(),
                'CcAddress': fake.email() if random.random() > 0.7 else None,
                'BccAddress': fake.email() if random.random() > 0.9 else None,
                'Status': random.choice(statuses),
                'Priority': random.choice(priorities),
                'MessageDate': fake.date_time_between(start_date='-2y', end_date='now'),
                'CreatedDate': fake.date_time_between(start_date='-2y', end_date='now'),
                'LastModifiedDate': fake.date_time_between(start_date='-1y', end_date='now'),
                'ActivityId': f'00T{fake.random_number(digits=15)}',  # Related Activity ID
                'ParentId': f'001{fake.random_number(digits=15)}',   # Related Case/Lead/Contact ID
                'MessageSize': len(body) + len(subject),
                'EmailType': email_type,
                'IsTracked': random.choice([True, False]),
                'IsOpened': random.choice([True, False]),
                'OpenCount': random.randint(0, 5) if random.random() > 0.3 else 0
            }
            
            emails.append(email_record)
            
            # Progress indicator for large batches
            if (i + 1) % 1000 == 0:
                print(f"Generated {i + 1} emails...")
        
        df = pd.DataFrame(emails)
        print(f"✅ Generated {len(df)} email records")
        return df
    
    def _generate_content_by_type(self, email_type):
        """Generate realistic subject and body based on email type"""
        
        if email_type == 'customer_inquiry':
            subjects = [
                f"Question about {fake.word().title()} Product",
                f"Need help with {fake.word()}",
                "Product Information Request",
                f"Inquiry about {fake.company()} services"
            ]
            body_templates = [
                f"Hello,\n\nI'm interested in learning more about your {fake.word()} services. Could you please provide more details about pricing and availability?\n\nBest regards,\n{fake.name()}",
                f"Hi there,\n\nI saw your {fake.word()} product online and have a few questions. When would be a good time to discuss this further?\n\nThanks,\n{fake.name()}"
            ]
            
        elif email_type == 'support_ticket':
            subjects = [
                f"Issue with {fake.word().title()} - Ticket #{fake.random_number(digits=6)}",
                "Technical Support Needed",
                f"Problem accessing {fake.word()} dashboard",
                "Account access issues"
            ]
            body_templates = [
                f"Hi Support Team,\n\nI'm experiencing an issue with {fake.word()} functionality. The error message shows: '{fake.sentence()}'\n\nSteps to reproduce:\n1. {fake.sentence()}\n2. {fake.sentence()}\n\nPlease advise.\n\n{fake.name()}",
                f"Hello,\n\nI cannot log into my account. I've tried resetting my password but still having issues. My account email is {fake.email()}.\n\nPlease help.\n\n{fake.name()}"
            ]
            
        elif email_type == 'sales_follow_up':
            subjects = [
                f"Following up on our {fake.month_name()} conversation",
                "Next steps for your project",
                f"Proposal for {fake.company()}",
                "Quick follow-up question"
            ]
            body_templates = [
                f"Hi {fake.first_name()},\n\nIt was great meeting with you last week. As discussed, I'm attaching the proposal for your {fake.word()} project.\n\nLet me know if you have any questions!\n\nBest,\n{fake.name()}",
                f"Hello {fake.first_name()},\n\nJust checking in to see if you had a chance to review the information I sent over. I'm here if you need any clarification.\n\nThanks,\n{fake.name()}"
            ]
            
        elif email_type == 'internal':
            subjects = [
                f"Team Meeting - {fake.date_object().strftime('%B %d')}",
                f"Update on {fake.word().title()} Project",
                "Weekly Status Report",
                f"{fake.word().title()} Process Documentation"
            ]
            body_templates = [
                f"Team,\n\nPlease find this week's status update below:\n\n• {fake.sentence()}\n• {fake.sentence()}\n• {fake.sentence()}\n\nLet me know if you have questions.\n\n{fake.name()}",
                f"Hi everyone,\n\nThe {fake.word()} project is progressing well. Current status:\n- Completed: {fake.sentence()}\n- In Progress: {fake.sentence()}\n- Next: {fake.sentence()}\n\nThanks,\n{fake.name()}"
            ]
            
        else:  # newsletter
            subjects = [
                f"{fake.month_name()} Newsletter - {fake.company()}",
                f"Weekly Update from {fake.company()}",
                "New Product Announcements",
                f"{fake.word().title()} Tips and Best Practices"
            ]
            body_templates = [
                f"Dear Subscriber,\n\nWelcome to our {fake.month_name()} newsletter! This month we're featuring:\n\n• {fake.sentence()}\n• {fake.sentence()}\n• {fake.sentence()}\n\nRead more at {fake.url()}\n\nBest regards,\nThe {fake.company()} Team",
                f"Hello,\n\nHere are this week's highlights:\n\n1. {fake.sentence()}\n2. {fake.sentence()}\n3. {fake.sentence()}\n\nVisit our blog for more details: {fake.url()}\n\nCheers,\n{fake.company()}"
            ]
        
        subject = random.choice(subjects)
        body = random.choice(body_templates)
        
        return subject, body
    
    def save_to_csv(self, df, filename):
        """Save DataFrame to CSV file"""
        filepath = f"data/{filename}"
        df.to_csv(filepath, index=False)
        file_size_mb = round(len(df) * df.memory_usage(deep=True).sum() / (1024*1024), 2)
        print(f"💾 Saved {len(df)} records to {filepath}")
        print(f"📊 File size: ~{file_size_mb} MB")
        return filepath

# Example usage
if __name__ == "__main__":
    generator = EmailMessageGenerator()
    
    # Generate different batch sizes for testing
    small_batch = generator.generate_email_batch(100)
    generator.save_to_csv(small_batch, "email_sample_100.csv")
    
    medium_batch = generator.generate_email_batch(5000)
    generator.save_to_csv(medium_batch, "email_sample_5000.csv")
    
    print("✅ Email data generation complete!")