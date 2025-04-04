from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app01.characters.services import CharacterService


@api_view(['GET'])
def find_character(request, character_id):
    """
    获取单个角色信息
    :param request: DRF请求对象
    :param character_id: 该角色的ID（来自URL路由）
    :return: JSON响应
    """
    try:
        # 1. 获取角色数据
        character_data = CharacterService.get_character(character_id)

        # 2. 处理空结果
        if not character_data:
            return Response(
                {'success': False, 'error': '不存在该ID的角色'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. 返回成功响应
        return Response(
            {'success': True, 'data': character_data},
            status=status.HTTP_200_OK
        )

    except ValueError as e:
        # 4. 处理业务逻辑错误
        return Response(
            {'success': False, 'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # 5. 处理未知错误
        return Response(
            {
                'success': False,
                'error': '服务器内部错误',
                'detail': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )