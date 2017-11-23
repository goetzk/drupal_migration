from __future__ import unicode_literals

from django.db import models


# TODO: Is this is current body, where FieldRevisionBody is all the previous revisions?
class FieldDataBody(models.Model):  # Approx 185 rows
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts or short thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # ignore, always 2
    revision_id = models.IntegerField(blank=True, null=True)  # NOTE: I don't think there is a central location for this, its just an identifier across tables
    language = models.CharField(max_length=32)                # ignore, unset
    delta = models.IntegerField()                             # ignore, always 0
    body_value = models.TextField(blank=True)                 # text, actual body
    body_summary = models.TextField(blank=True)               # ignore, always blank
    body_format = models.CharField(max_length=255, blank=True) # ignore, don't care about the html supportedness

    class Meta:
        managed = False
        db_table = 'field_data_body'

class FieldDataFieldFiles(models.Model): # files uploaded in to drupal. (5 rows, easier to manually move them)
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts or short thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # NOTE: Node.nid, any others?
    revision_id = models.IntegerField(blank=True, null=True)  # TODO: use this, specifies revision
    language = models.CharField(max_length=32)                # ignore, unset
    delta = models.IntegerField()                             # ignore, always 0
    field_files_fid = models.IntegerField(blank=True, null=True) # NOTE: FileManaged.fid
    field_files_display = models.IntegerField()               # Ignore, all 1
    field_files_description = models.TextField(blank=True)    # TODO: use this, some have text

    class Meta:
        managed = False
        db_table = 'field_data_field_files'

class FieldDataFieldTags(models.Model): # map between node/pages and taxonomy/tags. 630 rows
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # ignore, always 2
    revision_id = models.IntegerField(blank=True, null=True)  # NOTE: this changes
    language = models.CharField(max_length=32)                # ignore, undef
    delta = models.IntegerField()                             # ignore, changes but probably safe to ignore
    field_tags_tid = models.IntegerField(blank=True, null=True) # NOTE: TaxonomyTermData.tid

    class Meta:
        managed = False
        db_table = 'field_data_field_tags'


# NOTE: has more revision_id's than FieldDataBody. that has 181 and this 314 (revision id is 322, some missing? deleted?)
# If they are duplicate when they match, I don't need to look at FieldDataBody
class FieldRevisionBody(models.Model): # appears to contain history of all entities.
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


class FieldRevisionFieldFiles(models.Model): # 18 rows
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # NOTE: Node.nid
    revision_id = models.IntegerField()                       # NOTE: this changes
    language = models.CharField(max_length=32)                # ignore, always unde
    delta = models.IntegerField()                             # Varies, but will probably ignore it
    field_files_fid = models.IntegerField(blank=True, null=True) # NOTE: FileManaged.fid
    field_files_display = models.IntegerField()               # ignore, all 1
    field_files_description = models.TextField(blank=True)    # NOTE: some have text (description) in them

    class Meta:
        managed = False
        db_table = 'field_revision_field_files'

class FieldRevisionFieldTags(models.Model): # tags at a given revision. 1100 rows!
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

class FileManaged(models.Model): # 5 rows
    fid = models.IntegerField(primary_key=True)         # NOTE: referenced elsewhere
    uid = models.IntegerField()                         # ignore, always 1 (user id, presumably)
    filename = models.CharField(max_length=255)         # NOTE: files name, useful
    uri = models.CharField(unique=True, max_length=255) # ignore, just filename with public:// prefixed to it
    filemime = models.CharField(max_length=255)         # NOTE: mime type, might be useful?
    filesize = models.IntegerField()                    # ignore, size probably isn't relevant
    status = models.IntegerField()                      # ignore, all 1
    timestamp = models.IntegerField()                   # NOTE: probably a publication/upload stamp

    class Meta:
        managed = False
        db_table = 'file_managed'

class FileUsage(models.Model): # 5 rows
    fid = models.IntegerField()                         # NOTE: maps to FileManaged.fid
    module = models.CharField(max_length=255)           # ignore, all file
    type = models.CharField(max_length=64)              # ignore, all node
    id = models.IntegerField()                          # NOTE: node id (Node.nid) / page its on
    count = models.IntegerField()                       # ignore, not sure what this is for

    class Meta:
        managed = False
        db_table = 'file_usage'


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


# - node_revision for nid (node id; 'page'), vid (revision id?), title (page title), log, timestamp, status (published)  (312 rows)
#   select nid, vid, title, log, timestamp, status from node_revision;
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


class TaxonomyIndex(models.Model):  # 432 rows
    nid = models.IntegerField()                          # NOTE: use this, TODO: FK on Node.nid (node id)
    tid = models.IntegerField()                          # NOTE: use this, TODO: FK on TaxonomyTermData.tid (term id)
    sticky = models.IntegerField(blank=True, null=True)  # ignore, all 0
    created = models.IntegerField()                      # NOTE: use this , TODO: return as datettime

    class Meta:
        managed = False
        db_table = 'taxonomy_index'


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


