from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from app01.guides.GuidesService import GuidesService
import app01.tools.CalculateTools as tools
import logging

logger = logging.getLogger(__name__)  # 自动继承全局配置

"""
攻略相关视图函数集
"""


@api_view(['GET'])
def conventional_damage_calculation(request):
    print(request.query_params)
    pass


@api_view(['GET'])
def get_light_cones(request):
    pk = request.query_params.get('id', None)
    try:
        # 获取光锥数据
        light_cone_data = GuidesService.get_light_cone()
        for row in light_cone_data:
            row['light_cone_image_1'] = f"""/static/images/lightcone/{row.get('name')}.png"""
            row['path_img'] = f"""/static/images/general/paths/{row.get('paths')}.png"""
            # 备用名
            # row['light_cone_image_2'] = f"""/static/images/characters/{row.get('id')}/{row.get('name')}_2.png"""

        if not light_cone_data:
            logger.warning(f"光锥信息不存在 ID: {pk}")
            return render(request, 'guides_index.html', status=status.HTTP_404_NOT_FOUND)

        return Response({'total': 0, 'data': light_cone_data}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"页面渲染失败: {str(e)}")
        return render(request, 'guides_index.html', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
