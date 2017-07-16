import logging
import uuid

import celery
from celery.utils.log import get_task_logger
import kombu.message
from django.db import transaction

logger = get_task_logger(__name__)


@celery.shared_task(ignore_result=True)
def update_user(body, delivery_info, **kwargs):
    from idm_core.identity.models import Identity, User

    with transaction.atomic(savepoint=False):
        _, action, user_id = delivery_info['routing_key'].split('.')
        print(delivery_info['routing_key'])
        try:
            user_id = uuid.UUID(user_id)
        except ValueError:
            logger.exception("Bad user_id in routing key %s", delivery_info['routing_key'])
            raise
        if action in ('created', 'changed'):
            try:
                user = User.objects.filter(username=user_id).select_for_update().get()
            except User.DoesNotExist:
                user = User(username=user_id)
            # print(body)
            try:
                identity = Identity.objects.get(id=body['identity_id'])
            except Identity.DoesNotExist:
                logger.warning(
                    "Couldn't match identity for user {} (identity {})".format(body['id'], body['identity_id']))
                raise
            user.identity_id = identity.id
            user.identity_content_type = identity.content_type
            user.principal_name = body['principal_name']
            user.save()
            logger.info("User {}".format(action))
        elif action == 'deleted':
            for user in User.objects.filter(id=user_id):
                user.delete()
        else:
            raise AssertionError("Unexpected action in routing key %s", delivery_info['routing_key'])
