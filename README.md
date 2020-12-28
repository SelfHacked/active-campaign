# Active Campaign

This app contains a list of resources classes that ease the interaction with Active Campaign.

# Requirements

- django
- pytest
- requests

# Installation



# Basic Usage

```
from active_campaign import Contact, ContactList, ContactTag, Tag, MarketingList
```
## Contact

#### Create or get

```
contact = Contact(email)
try:
    contact.save()
except Exception:
    pass
```
#### Find by email

```
contact = Contact.find(email)
```

## Tag

#### Find by name
```
try:
  Tag.find("Tag name")
except Exception:
  # pass
```

#### Save or Update
```
tag = Tag('Tag name', 'contact', "Short description of the tag")
tag.save()
```

## MarketingList

#### Find by name
```
marketing_list = MarketingList.find('SD: Marketing List')
```

#### Save or update

## ContactTag

#### Attach tag to contact

```
ContactTag(tag.id, contact.id).save()
```

## ContactList

#### Subscribe/Unsubscribe contact to list
```
status = 1 #    1 to subscribe, 2 to unsubscribe
ContactList(marketing_list.id, contact.id, status).save()
```


# Settings

The plugin looks for the MARKETING_CAMPAIGN_KEY in django settings. It raises a RuntimeError if it's not correctly defined
