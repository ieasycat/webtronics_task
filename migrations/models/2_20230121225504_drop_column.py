from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "evaluation" DROP CONSTRAINT "fk_evaluati_user_d186717e";
        ALTER TABLE "evaluation" RENAME COLUMN "users_id" TO "user_id";
        ALTER TABLE "evaluation" ADD CONSTRAINT "fk_evaluati_user_6e218cd0" FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "evaluation" DROP CONSTRAINT "fk_evaluati_user_6e218cd0";
        ALTER TABLE "evaluation" RENAME COLUMN "user_id" TO "users_id";
        ALTER TABLE "evaluation" ADD CONSTRAINT "fk_evaluati_user_d186717e" FOREIGN KEY ("users_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""
