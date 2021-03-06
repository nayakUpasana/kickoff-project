"""empty message

Revision ID: c6aa0eff6528
Revises: ae6c0c723a02
Create Date: 2021-02-11 16:23:48.992078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6aa0eff6528'
down_revision = 'ae6c0c723a02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('academic_program',
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.Column('program_code', sa.String(), nullable=True),
    sa.Column('program_name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('program_id'),
    sa.UniqueConstraint('program_code')
    )
    op.create_table('student_program',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stu_username', sa.String(length=80), nullable=True),
    sa.Column('prog_code', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['prog_code'], ['academic_program.program_code'], ),
    sa.ForeignKeyConstraint(['stu_username'], ['student_names.student_username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_program')
    op.drop_table('academic_program')
    # ### end Alembic commands ###
