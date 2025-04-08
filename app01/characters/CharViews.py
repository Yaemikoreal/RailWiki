from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from app01.characters.Services import CharacterService
import app01.tools.CalculateTools as tools
import logging

logger = logging.getLogger(__name__)  # 自动继承全局配置

"""
角色相关视图函数集
"""


@api_view(['GET'])
def character_detail(request, pk):
    """
    获取单个角色信息
    :param pk:
    :param request: DRF请求对象
    :return: JSON响应
    """
    character_id = pk
    try:
        character_data = CharacterService.get_character_msg(character_id)

        if not character_data:
            result_msg = "不存在该ID的角色"
            logger.info(result_msg)
            return Response(result_msg, status=status.HTTP_404_NOT_FOUND)

        logger.info("查询角色信息成功!")
        return Response(character_data, status=status.HTTP_200_OK)

    except ValueError as e:
        logger.error(f"查询出错:{str(e)}")
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"查询出错(服务器内部错误):{str(e)}")
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        logger.info(f"[{data_dt}]查询成功!", {'total': len(characters_data_lt), 'characters': characters_data_lt})
        return Response({'total': len(characters_data_lt), 'characters': characters_data_lt}, status=status.HTTP_200_OK)
    except ValueError as e:
        logger.error(f"查询出错:{str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(str(e))


@api_view(['GET'])
def show_character_detail(request):
    """
    角色详情页渲染视图
    同时预加载基础数据避免二次请求
    """
    pk = request.query_params.get('id', None)
    try:
        # 获取基础角色数据
        character_data = CharacterService.get_character_msg(pk)

        if not character_data:
            logger.warning(f"角色不存在 ID: {pk}")
            return render(request, 'wiki_index.html', status=status.HTTP_404_NOT_FOUND)

        # 构造响应数据
        context = {
            'character_id': pk,
            'character': character_data  # 预加载数据
        }
        return render(request, 'character_detail.html', context)

    except Exception as e:
        logger.error(f"页面渲染失败: {str(e)}")
        return render(request, 'wiki_index.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def find_character_talent(request, char_id):
    """
    查询单个角色天赋技能信息
    :param char_id: 需要查询的角色ID
    :param request:
    :return:
    """
    try:
        talent_data_tuple = CharacterService.get_character_talent(char_id)
        # 整理角色技能信息数据结构
        talent_data = tools.calculate_talents(talent_data_tuple)

        if not talent_data:
            result_msg = "不存在该角色的技能信息"
            logger.info(result_msg)
            return Response(result_msg, status=status.HTTP_404_NOT_FOUND)

        logger.info("查询角色技能信息成功!")
        return Response(talent_data, status=status.HTTP_200_OK)

    except ValueError as e:
        logger.error(f"查询出错:{str(e)}")
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"查询出错(服务器内部错误):{str(e)}")
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def find_characters_constellation(request, char_id):
    """
        查询单个角色星魂信息查询
        :param char_id: 需要查询的角色ID
        :param request:
        :return:
        """
    try:
        constellation_data_tuple = CharacterService.get_character_constellation(char_id)
        constellation_data = tools.calculate_constellation(constellation_data_tuple)
        if not constellation_data:
            result_msg = "不存在该角色的星魂信息"
            logger.info(result_msg)
            return Response(result_msg, status=status.HTTP_404_NOT_FOUND)

        logger.info("查询角色星魂信息成功!")
        return Response(constellation_data, status=status.HTTP_200_OK)

    except ValueError as e:
        logger.error(f"查询出错:{str(e)}")
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"查询出错(服务器内部错误):{str(e)}")
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
