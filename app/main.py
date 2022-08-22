from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pyristic.utils import get_stats
from .argument_types import EvolutionaryAlgorithm, EvolutionaryOperators, FileType, StringInput, OptimizerArguments
from .validations import ValidateFiles
from .utils import create_evolutionary_config, create_file, create_evolutionary_algorithm, transform_values_dict
from .settings import OAPI_TAGS

app = FastAPI(
    title='pyristic-api',
    description="API to create files related to the optimization \
        problem and perform one of the search algorithm that has pyristic.",
    docs_url='/',
    openapi_tags=OAPI_TAGS
)

@app.post(
    "/create-file/{file_name}",
    status_code=200,
    tags=["Utilities"])
def create_file_request(file_name: FileType, text_content: StringInput):
    """
    Description:
        It creates a file with the content.
    Arguments:
        - file_name: string indicating the file name where to save the content.
        - text_content: string with python code. This content is saved as a python file.
    """
    try:
        create_file(file_name, text_content.content)
    except:
        raise HTTPException(
                status_code= 500,
                detail= f"Something happend in the creation of {file_name}."
            )
    return f"Created with success {file_name}"

@app.post(
    "/optimize/evolutionary/{optimizer}",
    status_code=200,
    dependencies = [Depends(ValidateFiles(['function', 'constraints','search_space']))],
    tags=["Evolutionary optimization algorithm"])
def execute_optimizer_request(
    optimizer: EvolutionaryAlgorithm,
    num_executions: int,
    arguments_optimizer: OptimizerArguments,
    config_operators: EvolutionaryOperators):
    """
    Description:
    This is the route to execute an evolutionary algorithm with the specified configuration
    specific number of executions.
    Arguments:
        - optimizer: the evolutionary algorithm selected.
        - num_executions: integer number that is the number of times executed the algorithm.
        - arguments_optimizer: dictionary with the key arguments for the optimize method.
        - config_operators: dictionary with the operators applied to the algorithm.
    """
    configuration = create_evolutionary_config(optimizer, config_operators.methods)
    evolutionary_algorithm = create_evolutionary_algorithm(optimizer, configuration)
    statistics_algorithm = transform_values_dict(
                            get_stats(
                                evolutionary_algorithm,
                                num_executions,
                                [],
                                arguments_optimizer.arguments,
                                verbose=False
                            )
                        )
    return JSONResponse(content=statistics_algorithm)

