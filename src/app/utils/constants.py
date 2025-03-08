
class DatabaseConstants:
    CONNECTION_TIMEOUT = 30
    POOL_SIZE = 10


class BusinessLogicConstants:
    MAX_ITEM_QUANTITY = 100
    DISCOUNT_RATE = 0.1  # 10%

class BusinessCtrlParaConstants:
    APP_NAME = "opt"
    PARAM_TYPE_FLOAT = 1
    PARAM_NAME_FOR_TRIGGER_TIMESPAN = "OptTriggerTimeSpan"
    PARAM_NAME_FOR_TRIGGER_SOC_THRESHOLD="OptTriggerSOCThreshold"
    PARAM_NAME_FOR_TRIGGER_DISTANCE_THRESHOLD="TriggerDistanceThreshold"

    DEFAULT_PARA_VALUES={
        PARAM_NAME_FOR_TRIGGER_TIMESPAN: 60,
        PARAM_NAME_FOR_TRIGGER_SOC_THRESHOLD: 20,
        PARAM_NAME_FOR_TRIGGER_DISTANCE_THRESHOLD: 10,
    }
    PARAM_COMMENTS={
        PARAM_NAME_FOR_TRIGGER_TIMESPAN: "触发时间间隔 单位：分钟",
        PARAM_NAME_FOR_TRIGGER_SOC_THRESHOLD: "触发SOC阈值 单位：%",
        PARAM_NAME_FOR_TRIGGER_DISTANCE_THRESHOLD: "触发距离阈值 单位：km",
    }

class ErrorType:
    """
    错误类型
    """
    # 通用错误
    COMMON = 'COMMON'
    # 数据库错误
    DATABASE = 'Database Error'
    # 业务逻辑错误
    BUSINESS = 'BUSINESS'
    # 参数错误
    PARAMETER = 'PARAMETER'
    # 未知错误
    UNKNOWN = 'UNKNOWN'

class TSTableFieldNames():
    # ID: str = "ID"
    BusCode: str = "BusCode"
    DataSource: str = "DataSource"

    CurrentTime:str="ts"
    DepCode: str = "DepCode"
    LineCode: str = "LineCode"
    DriverCode: str = "DriverCode"
    RecentStopCode: str = "RecentStopCode"
    SpeedPerHour: str = "SpeedPerHour"
    Longitude: str = "Longitude"
    Latitude: str = "Latitude"
    KilometerageToday: str = "KilometerageToday"
    PlanTripsToday: str = "PlanTripsToday"
    ActualTripsToday: str = "ActualTripsToday"
    ActualDepartureTime: str = "ActualDepartureTime"
    RunningFlag: str = "RunningFlag"
    BusStatus: str = "BusStatus"

    KEY_TYPE: str = "VARCHAR(36)"
    DATETIME_TYPE: str = "TIMESTAMP"
    FLOAT_TYPE: str = "FLOAT"
    INT_TYPE: str = "INT"
    SMALLINT_TYPE: str = "SMALLINT"


class TDTableInfo():
    """
    时序数据库表信息
    """
    table_name_prefix = "Bus"
    db_name = "BusOpt"
    stable_name = "CurrentStatus"
    # CREATE STABLE meters (ts timestamp, current float, voltage int, phase float) TAGS (location binary(64), groupId int);
    metrics=f"({TSTableFieldNames.CurrentTime} {TSTableFieldNames.DATETIME_TYPE}, " \
            f"{TSTableFieldNames.DepCode} {TSTableFieldNames.KEY_TYPE}, " \
            f"{TSTableFieldNames.LineCode} {TSTableFieldNames.KEY_TYPE}, " \
            f"{TSTableFieldNames.DriverCode} {TSTableFieldNames.KEY_TYPE}, " \
            f"{TSTableFieldNames.RecentStopCode} {TSTableFieldNames.KEY_TYPE}, " \
            f"{TSTableFieldNames.SpeedPerHour} {TSTableFieldNames.FLOAT_TYPE}, " \
            f"{TSTableFieldNames.Longitude} {TSTableFieldNames.FLOAT_TYPE}, " \
            f"{TSTableFieldNames.Latitude} {TSTableFieldNames.FLOAT_TYPE}, " \
            f"{TSTableFieldNames.KilometerageToday} {TSTableFieldNames.FLOAT_TYPE}, " \
            f"{TSTableFieldNames.PlanTripsToday} {TSTableFieldNames.INT_TYPE}, " \
            f"{TSTableFieldNames.ActualTripsToday} {TSTableFieldNames.INT_TYPE}, " \
            f"{TSTableFieldNames.ActualDepartureTime} {TSTableFieldNames.DATETIME_TYPE}, " \
            f"{TSTableFieldNames.RunningFlag} {TSTableFieldNames.SMALLINT_TYPE}, " \
            f"{TSTableFieldNames.BusStatus} {TSTableFieldNames.SMALLINT_TYPE})"
    tags = f"TAGS ( {TSTableFieldNames.BusCode} {TSTableFieldNames.KEY_TYPE}, " \
           f"{TSTableFieldNames.DataSource} {TSTableFieldNames.SMALLINT_TYPE})"
    CREATE_DATABASE_STATEMENT = f"CREATE DATABASE {db_name} KEEP 30 DURATION 1 BUFFER 16 WAL_LEVEL 1;"
    CREATE_STABLE_STATEMENT = f"CREATE STABLE {db_name}.{stable_name} {metrics} {tags};"

