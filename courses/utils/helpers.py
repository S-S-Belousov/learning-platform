from datetime import datetime
from math import ceil

from django.db import transaction


@transaction.atomic
def distribute_users_to_groups_helper(product):
    if not product.users_with_access.filter(id=product.creator.id).exists():
        return
    if product.start_datetime > datetime.now():
        groups = product.group_set.all().order_by('id')
        num_groups = groups.count()
        print(num_groups)
        if num_groups == 0:
            return
        students = product.creator.profile.groups_assigned.all().order_by('id')
        num_students = students.count()
        min_group_size = product.min_group_size
        max_group_size = product.max_group_size
        ideal_group_size = ceil(num_students / num_groups)
        min_group_size = min(min_group_size, ideal_group_size)
        max_group_size = min(max_group_size, ideal_group_size + 1)

        start_idx = 0
        for idx, group in enumerate(groups):
            end_idx = min(start_idx + max_group_size, num_students)
            group_size = min(max_group_size, end_idx - start_idx)
            if group_size < min_group_size:
                group_size = min_group_size
            group_students = students[start_idx:start_idx + group_size]
            group.students.set(group_students)
            group.save()
            start_idx += group_size
        groups[num_students:].delete()
