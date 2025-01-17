#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：MaxKB 
@File    ：gemini_model_provider.py
@Author  ：Brian Yang
@Date    ：5/13/24 7:47 AM 
"""
import os

from common.util.file_util import get_file_content
from setting.models_provider.base_model_provider import IModelProvider, ModelProvideInfo, ModelInfo, ModelTypeConst, \
    ModelInfoManage
from setting.models_provider.impl.openai_model_provider.credential.embedding import OpenAIEmbeddingCredential
from setting.models_provider.impl.openai_model_provider.credential.llm import OpenAILLMModelCredential
from setting.models_provider.impl.openai_model_provider.model.embedding import OpenAIEmbeddingModel
from setting.models_provider.impl.volcanic_engine_model_provider.credential.image import \
    VolcanicEngineImageModelCredential
from setting.models_provider.impl.volcanic_engine_model_provider.credential.tti import VolcanicEngineTTIModelCredential
from setting.models_provider.impl.volcanic_engine_model_provider.credential.tts import VolcanicEngineTTSModelCredential
from setting.models_provider.impl.volcanic_engine_model_provider.model.image import VolcanicEngineImage
from setting.models_provider.impl.volcanic_engine_model_provider.model.llm import VolcanicEngineChatModel
from setting.models_provider.impl.volcanic_engine_model_provider.credential.stt import VolcanicEngineSTTModelCredential
from setting.models_provider.impl.volcanic_engine_model_provider.model.stt import VolcanicEngineSpeechToText
from setting.models_provider.impl.volcanic_engine_model_provider.model.tti import VolcanicEngineTextToImage
from setting.models_provider.impl.volcanic_engine_model_provider.model.tts import VolcanicEngineTextToSpeech

from smartdoc.conf import PROJECT_DIR

volcanic_engine_llm_model_credential = OpenAILLMModelCredential()
volcanic_engine_stt_model_credential = VolcanicEngineSTTModelCredential()
volcanic_engine_tts_model_credential = VolcanicEngineTTSModelCredential()
volcanic_engine_image_model_credential = VolcanicEngineImageModelCredential()
volcanic_engine_tti_model_credential = VolcanicEngineTTIModelCredential()

model_info_list = [
    ModelInfo('ep-xxxxxxxxxx-yyyy',
              '用户前往火山方舟的模型推理页面创建推理接入点，这里需要输入ep-xxxxxxxxxx-yyyy进行调用',
              ModelTypeConst.LLM,
              volcanic_engine_llm_model_credential, VolcanicEngineChatModel
              ),
    ModelInfo('ep-xxxxxxxxxx-yyyy',
              '用户前往火山方舟的模型推理页面创建推理接入点，这里需要输入ep-xxxxxxxxxx-yyyy进行调用',
              ModelTypeConst.IMAGE,
              volcanic_engine_image_model_credential, VolcanicEngineImage
              ),
    ModelInfo('asr',
              '',
              ModelTypeConst.STT,
              volcanic_engine_stt_model_credential, VolcanicEngineSpeechToText
              ),
    ModelInfo('tts',
              '',
              ModelTypeConst.TTS,
              volcanic_engine_tts_model_credential, VolcanicEngineTextToSpeech
              ),
    ModelInfo('general_v2.0',
              '通用2.0-文生图',
              ModelTypeConst.TTI,
              volcanic_engine_tti_model_credential, VolcanicEngineTextToImage
              ),
    ModelInfo('general_v2.0_L',
              '通用2.0Pro-文生图',
              ModelTypeConst.TTI,
              volcanic_engine_tti_model_credential, VolcanicEngineTextToImage
              ),
    ModelInfo('general_v1.4',
              '通用1.4-文生图',
              ModelTypeConst.TTI,
              volcanic_engine_tti_model_credential, VolcanicEngineTextToImage
              ),
    ModelInfo('anime_v1.3',
              '动漫1.3.0-文生图',
              ModelTypeConst.TTI,
              volcanic_engine_tti_model_credential, VolcanicEngineTextToImage
              ),
    ModelInfo('anime_v1.3.1',
              '动漫1.3.1-文生图',
              ModelTypeConst.TTI,
              volcanic_engine_tti_model_credential, VolcanicEngineTextToImage
              ),
]

open_ai_embedding_credential = OpenAIEmbeddingCredential()
model_info_embedding_list = [
    ModelInfo('ep-xxxxxxxxxx-yyyy',
              '用户前往火山方舟的模型推理页面创建推理接入点，这里需要输入ep-xxxxxxxxxx-yyyy进行调用',
              ModelTypeConst.EMBEDDING, open_ai_embedding_credential,
              OpenAIEmbeddingModel)]

model_info_manage = (
    ModelInfoManage.builder()
    .append_model_info_list(model_info_list)
    .append_default_model_info(model_info_list[0])
    .append_default_model_info(model_info_list[1])
    .append_default_model_info(model_info_list[2])
    .append_default_model_info(model_info_list[3])
    .append_default_model_info(model_info_list[4])
    .build()
)


class VolcanicEngineModelProvider(IModelProvider):

    def get_model_info_manage(self):
        return model_info_manage

    def get_model_provide_info(self):
        return ModelProvideInfo(provider='model_volcanic_engine_provider', name='火山引擎', icon=get_file_content(
            os.path.join(PROJECT_DIR, "apps", "setting", 'models_provider', 'impl', 'volcanic_engine_model_provider',
                         'icon',
                         'volcanic_engine_icon_svg')))
