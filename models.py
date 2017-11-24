from __future__ import unicode_literals

from django.db import models

class Node(models.Model): # 180 rows
    nid = models.IntegerField(primary_key=True)                     # NOTE: use this, nodes unique ID
    vid = models.IntegerField(unique=True, blank=True, null=True)   # NOTE: revision_id in other places
    type = models.CharField(max_length=32)                          # ignore, just extended/short thoughts
    language = models.CharField(max_length=12)                      # ignore, all undef
    title = models.CharField(max_length=255)                        # NOTE: use this, its text
    uid = models.IntegerField()                                     # ignore, all 1
    status = models.IntegerField()                                  # NOTE: published yes/no (1/0)
    created = models.IntegerField()                                 # NOTE: use this
    changed = models.IntegerField()                                 # NOTE: use this
    comment = models.IntegerField()                                 # ignore, all 0
    promote = models.IntegerField()                                 # ignore, i wasn't really using this properly
    sticky = models.IntegerField()                                  # ignore, all 0
    tnid = models.IntegerField()                                    # ignore, all 0
    translate = models.IntegerField()                               # ignore, all 0
    
    class Meta:
        managed = False
        db_table = 'node'

class NodeRevision(models.Model): # 317 rows
    nid = models.IntegerField()                     # NOTE: Node.nid
    vid = models.IntegerField(primary_key=True)     # NOTE: current revision, maps to revision_id elsewhere
    uid = models.IntegerField()                     # ignore, all 0
    title = models.CharField(max_length=255)        # NOTE: use this
    log = models.TextField()                        # NOTE: use this
    timestamp = models.IntegerField()               # NOTE: use this
    status = models.IntegerField()                  # ignore, published yes/no (1/0)
    comment = models.IntegerField()                 # ignore, all 0
    promote = models.IntegerField()                  # ignore, not using anyway
    sticky = models.IntegerField()                  # ignore, all 0
    
    class Meta:
        managed = False
        db_table = 'node_revision'

class TaxonomyTermData(models.Model): # 210 rows
    tid = models.IntegerField(primary_key=True)         # NOTE: unique id, referenced elsewhere
    vid = models.IntegerField()                         # ignore, all set to 1 (i haven't edited my tags)
    name = models.CharField(max_length=255)             # NOTE: keyword for tag
    description = models.TextField(blank=True)          # NOTE: description of tag
    format = models.CharField(max_length=255, blank=True) # ignore
    weight = models.IntegerField()                      # ignore
    
    class Meta:
        managed = False
        db_table = 'taxonomy_term_data'


class FieldDataFieldTags(models.Model): # map between node/pages and taxonomy/tags. 630 rows
    # Magic django managed primary_key, see README
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # ignore, always 2
    revision_id = models.IntegerField(blank=True, null=True)  # NOTE: 182 revisions, consistent with FieldDataBody but not useful as a PK
    language = models.CharField(max_length=32)                # ignore, undef
    delta = models.IntegerField()                             # ignore, changes but probably safe to ignore
    field_tags_tid = models.IntegerField(blank=True, null=True) # NOTE: TaxonomyTermData.tid

    class Meta:
        managed = False
        db_table = 'field_data_field_tags'

# NOTE: has more revision_id's than FieldDataBody. that has 181 and this 314 (revision id is 322, some missing? deleted?)
# If they are duplicate when they match, I don't need to look at FieldDataBody
class FieldRevisionBody(models.Model): # appears to contain history of all entities.
    # Magic django managed primary_key, see README
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # NOTE: Node.nid
    revision_id = models.IntegerField()                       # NOTE: this changes, ties to all other revision_id's
    language = models.CharField(max_length=32)                # ignore, always undef
    delta = models.IntegerField()                             # ignore, always 0
    body_value = models.TextField(blank=True)                 # NOTE: use this, contains full text of ody
    body_summary = models.TextField(blank=True)               # ignore, always blank
    body_format = models.CharField(max_length=255, blank=True) # ignore, full vs limited html; don't care

    class Meta:
        managed = False
        db_table = 'field_revision_body'

class FieldRevisionFieldTags(models.Model): # tags at a given revision. 1100 rows!
    # Magic django managed primary_key, see README
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # NOTE: Node.nid
    revision_id = models.IntegerField()                       # NOTE: this changes
    language = models.CharField(max_length=32)                # ignore, always unde
    delta = models.IntegerField()                             # Varies, but will probably ignore it
    field_tags_tid = models.IntegerField(blank=True, null=True) # NOTE: TaxonomyTermData.tid

    class Meta:
        managed = False
        db_table = 'field_revision_field_tags'

