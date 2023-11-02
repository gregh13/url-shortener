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
    original_url = UnicodeAttribute(attr_name="OriginalUrl")

# # Item creation, already done
# new_item = Thread(short_url='ex_short', original_url="ex_reallllly_looonnngg")
# new_item.save()

check_item_in_db = Thread.get("ex_short")
print(f"Item pulled from local database: \n"
      f"Short Url: {check_item_in_db.short_url}\n"
      f"Original Url: {check_item_in_db.original_url}\n")


try:
    fake_url = "my_fake_url"
    check_fake_item = Thread.get(fake_url)
    print(check_fake_item)
except Thread.DoesNotExist:
    print(f"'{fake_url}' does not exist in database")