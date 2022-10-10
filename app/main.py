from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pyristic.utils import get_stats
import search_utils.evolutionary as EA_utils
import search_utils.simulated_annealing as SA_utils
import argument_types as arg_api
import validations as val_api
import utils
import settings

app = FastAPI(
    title='pyristic-api',
    description="API to create files related to the optimization \
        problem and perform one of the search algorithm that has pyristic.",
    docs_url='/',
    openapi_tags=settings.OAPI_TAGS
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/create-file/{file_name}",
    status_code=200,
    tags=["Utilities"])
def create_file_request(file_name: arg_api.FileType, text_content: arg_api.StringInput):
    """
    Description:
        It creates a file with the content.
    Arguments:
        - file_name: string indicating the file name where to save the content.
        - text_content: string with python code. This content is saved as a python file.
    """
    try:
        utils.create_file(file_name, text_content.content)
    except Exception as exc:
        raise HTTPException(
                status_code= 500,
                detail= str(exc)
            ) from exc
    return f"Created with success {file_name}"

@app.post(
    "/optimize/evolutionary/{optimizer}",
    status_code=200,
    dependencies = [Depends(val_api.ValidateFiles(['function', 'constraints','search_space']))],
    tags=["Evolutionary optimization algorithm"])
def execute_optimizer_request(
    optimizer: arg_api.EvolutionaryAlgorithm,
    num_executions: int,
    arguments_optimizer: arg_api.OptimizerArguments,
    config_operators: arg_api.EvolutionaryOperators):
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
    print("Starting evolutionary optimization execution")
    configuration = EA_utils.create_evolutionary_config(optimizer, config_operators.methods)
    print(configuration)
    evolutionary_algorithm = EA_utils.create_evolutionary_algorithm(optimizer, configuration)
    print("Created evolutionary algorithm")
    statistics_algorithm = utils.transform_values_dict(
                            get_stats(
                                evolutionary_algorithm,
                                num_executions,
                                [],
                                arguments_optimizer.arguments,
                                verbose=True
                            )
                        )
    print("End evolutionary optimization execution")
    return JSONResponse(content=statistics_algorithm)


@app.post(
        "/optimize/SimulatedAnnealing",
        status_code=200,
        dependencies = [Depends(val_api.ValidateFiles(
                            [
                            'function',
                            'constraints',
                            'SA_neighbor_generator',
                            'generator_initial_solution'
                            ]))
                        ],
        tags=["Combinatorial algorithms"]
    )
def execute_sa_request(num_executions:int, arguments_optimizer: arg_api.OptimizerArguments):
    """
    Description:
        This is the route to execute a search based on Simulated Annealing implemented in pyristic.
    Arguments:
        - num_executions: integer number that is the number of times executed the algorithm.
        - arguments_optimizer: dictionary with the key arguments for the optimize method.
    """
    try:
        print("Starting SA optimization execution")
        get_initial_solution = utils.ModulesHandler().get_method_by_module(
                                    'generator_initial_solution',
                                    'generate_initial_solution'
                                )
        sa_algorithm = SA_utils.create_simulatedannealing_algorithm()
        print("created SA algorithm")
        statistics_algorithm = utils.transform_values_dict(
                            get_stats(
                                sa_algorithm,
                                num_executions,
                                [get_initial_solution],
                                arguments_optimizer.arguments,
                                verbose=True
        ))
        print("End SA optimization execution")
    except Exception as exc:
        print("Error:", exc)
        raise HTTPException(
            status_code= 404,
            detail= str(exc)
        ) from exc
    return JSONResponse(content=statistics_algorithm)


@app.post(
    "/pyristic/connected",
    status_code=200
)
def get_verification_response():
    """
    Auxiliar function to test the service is working.
    """
    return JSONResponse(content={'pyristic':'isAlive'})
