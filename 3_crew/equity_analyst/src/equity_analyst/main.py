from ast import Eq
from pathlib import Path
from dotenv import load_dotenv
from equity_analyst.crew import EquityAnalyst

_CURRENT_FILE = Path(__file__).resolve()
_ROOT_ENV = _CURRENT_FILE.parents[4] / ".env"
_PROJECT_ENV = _CURRENT_FILE.parents[2] / ".env"
for env_file in (_ROOT_ENV, _PROJECT_ENV):
    if env_file.exists():
        load_dotenv(env_file, override=True)

def run():
    """
    Run Research Crew
    """

    inputs ={
        'sector':'Technology'
    }

    result=EquityAnalyst().crew().kickoff(inputs=inputs)

    print("\n\n=== FINAL DECISION===\n\n")
    print(result.raw)


if __name__=="__main__":
    run()
