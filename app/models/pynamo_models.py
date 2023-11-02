from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Thread(Model):
    class Meta:
        table_name = 'URL'
        # Specifies the region
        region = 'us-east-2'
        # Optional: Specify the hostname only if it needs to be changed from the default AWS setting
        host = 'http://localhost:8000'
        # Specifies the write capacity
        write_capacity_units = 10
        # Specifies the read capacity
        read_capacity_units = 5

    short_url = UnicodeAttribute(hash_key=True, attr_name="ShortUrl")
    original_url = UnicodeAttribute(range_key=True, attr_name="OriginalUrl")
