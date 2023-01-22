from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "evaluation_user";
        DROP TABLE IF EXISTS "evaluation_post";
        ALTER TABLE "evaluation" ADD "users_id" INT NOT NULL;
        ALTER TABLE "evaluation" ADD "post_id" INT NOT NULL;
        ALTER TABLE "evaluation" ADD CONSTRAINT "fk_evaluati_post_59892ab5" FOREIGN KEY ("post_id") REFERENCES "post" ("id") ON DELETE CASCADE;
        ALTER TABLE "evaluation" ADD CONSTRAINT "fk_evaluati_user_d186717e" FOREIGN KEY ("users_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "evaluation" DROP CONSTRAINT "fk_evaluati_user_d186717e";
        ALTER TABLE "evaluation" DROP CONSTRAINT "fk_evaluati_post_59892ab5";
        ALTER TABLE "evaluation" DROP COLUMN "users_id";
        ALTER TABLE "evaluation" DROP COLUMN "post_id";
        CREATE TABLE "evaluation_post" (
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "evaluation_id" INT NOT NULL REFERENCES "evaluation" ("id") ON DELETE CASCADE
);
        CREATE TABLE "evaluation_user" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "evaluation_id" INT NOT NULL REFERENCES "evaluation" ("id") ON DELETE CASCADE
);"""
