from django.conf import settings
from estates.constants import ESTATE_COLLECTION_NAME
from pymongo import ASCENDING, DESCENDING, MongoClient, UpdateOne

from real_state.schema import EstateBase


def get_sort(sort: list) -> list:
    if sort is None:
        return []
    return [
        (d["field"], ASCENDING if "ASC" == d.get("ordering", "ASC") else DESCENDING)
        for d in sort
    ]


class MongoDB:
    def __init__(self):
        self.client = MongoClient(
            settings.MONGO_URL,
            username=settings.MONGO_DB_USER,
            password=settings.MONGO_DB_PASSWORD,
            retryWrites=False,
        )
        self.db = self.client[settings.MONGO_DB_DATABASE]
        self.estates_collection = self.db[ESTATE_COLLECTION_NAME]

    def filter_estates(self, filter_estates: dict, sort: list = None):
        if sort is None:
            return self.estates_collection.find(filter_estates)
        sort_by = get_sort(sort)
        return self.estates_collection.find(filter_estates).sort(sort_by)

    def delete_one_estate(self, estate_id: str):
        return self.estates_collection.delete_one({"_id": estate_id})

    def get_all_estates(self):
        return self.estates_collection.find()

    def remove_entire_collection(self):
        return self.estates_collection.drop()

    def update_many_estates(self, estates: list[EstateBase]):
        try:
            update_operations = []
            for estate in estates:
                update_operations.append(
                    UpdateOne(
                        {"_id": estate["id"]},
                        {"$set": estate},
                        upsert=True,
                    )
                )
            return self.estates_collection.bulk_write(update_operations)

        except Exception as e:
            raise e

    def create_or_update_estate(self, estate: EstateBase):
        try:
            return self.estates_collection.update_one(
                {"_id": estate["id"]},
                {"$set": estate},
                upsert=True,
            )
        except Exception as e:
            raise e


def get_paginator_mongo(
    collection, filter_mongo, page_size, page, paginated_type, order_by=None, **kwargs
):
    try:
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        total_results = collection.count_documents(filter_mongo)

        if order_by:
            results = (
                collection.find(filter_mongo)
                .sort(get_sort(order_by))
                .skip(start_index)
                .limit(page_size)
            )
        else:
            results = collection.find(filter_mongo).skip(start_index).limit(page_size)

        paginator = paginated_type(
            page=page,
            pages=(total_results + page_size - 1) // page_size,
            has_next=end_index < total_results,
            has_prev=start_index > 0,
            total_results=total_results,
            order_by=order_by,
            objects=list(results),
            **kwargs,
        )

        return paginator
    except Exception:
        return paginated_type(
            page=0,
            pages=0,
            has_next=False,
            has_prev=False,
            total_results=0,
            order_by=None,
            objects=[],
            **kwargs,
        )


mongodb = MongoDB()
