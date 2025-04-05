from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from app01.characters.Services import CharacterService
import logging

logger = logging.getLogger(__name__)  # 自动继承全局配置


@api_view(['GET'])
def find_character(request):
    """
    获取单个角色信息
    :param request: DRF请求对象
    :return: JSON响应
    """
    character_id = request.data.get('character_id')
    try:
        # 1. 获取角色数据
        character_data = CharacterService.get_character_msg(character_id)

        # 2. 处理空结果
        if not character_data:
            result_msg = "不存在该ID的角色"
            logger.info(result_msg)
            return Response(
                {'success': False, 'error': result_msg},
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. 返回成功响应
        logger.info("查询角色信息成功!")
        return Response(
            {'success': True, 'data': character_data},
            status=status.HTTP_200_OK
        )

    except ValueError as e:
        # 4. 处理业务逻辑错误
        logger.error(f"查询出错:{str(e)}")
        return Response(
            {'success': False, 'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error(f"查询出错(服务器内部错误):{str(e)}")
        # 5. 处理未知错误
        return Response(
            {
                'success': False,
                'error': '服务器内部错误',
                'detail': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def find_characters_list(request):
    """
    角色列表分页查询 API
    :param request:
    :return:
    """

    data_dt = request.data
    if not data_dt:

        data_dt = {
            'elements': request.query_params.get('elements'),
            'paths': request.query_params.get('paths'),
            'rarities': request.query_params.get('rarities'),
        }
    try:
        # characters_data_lt = CharacterService.get_characters_list_dan(data_dt)
        characters_data_lt = CharacterService.get_characters_list(data_dt)
        if not characters_data_lt:
            return Response({'total': 0, 'data': characters_data_lt}, status=status.HTTP_200_OK)
        logger.info("查询成功!", {'total': len(characters_data_lt), 'characters': characters_data_lt})
        return Response({'total': len(characters_data_lt), 'characters': characters_data_lt}, status=status.HTTP_200_OK)
    except ValueError as e:
        logger.error(f"查询出错:{str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(str(e))
