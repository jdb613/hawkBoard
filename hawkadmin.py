"""Application entry point."""
from app import create_app, db
from app.models import Transaction, Budget

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Transaction': Transaction, 'Budget': Budget}
