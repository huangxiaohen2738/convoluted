import factory.alchemy
from factory.base import FactoryMetaClass

suffix = "Factory"
mock_prefix = "mock_"


# register的本质其实是import module,
# 因此如果定义在其他地方，那么就只会在对应的模块内引用, 因此在全局的conftest中引用。
# 对于全局四处声明的mock data, 非常杂乱, 因此用factory统一声明, 而在使用的时候对于特定字段进行修改
# 可以使用 pytest.mark.parametrize 对特定对象的attribute进行修改
# 如:
# @pytest.mark.parametrize("mock_user__username", ["special-username"])
# def test_user(mock_user):
#     do test
# 或:
# @pytest.fixture
# def mock_user__roles(mock_role):
#    return [mock_role]
# from pytest_factoryboy import register
# factory 为 设置factoryboy的文件夹
# for factory_class, name in find_factory_module(factory):
#     register(factory_class, name)


class FactoryMixin(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        # 需要指明db.session
        # sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


def get_lower_case_name(text):
    text = text.replace(suffix, "")
    lst = [mock_prefix]
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            lst.append("_")
        lst.append(char)
    return "".join(lst).lower()


def find_factory_module(module):
    register_factories = []
    for name in dir(module):
        if name.startswith("__") and name.endswith("__"):
            continue
        factory_module = module.__dict__[name]
        for factory_class_name in dir(factory_module):
            if factory_class_name.endswith(suffix):
                factory_class = factory_module.__dict__[factory_class_name]
                if not isinstance(factory_class, FactoryMetaClass):
                    continue
                mock_factory_name = get_lower_case_name(factory_class_name)
                register_factories.append((factory_class, mock_factory_name))
    return register_factories
