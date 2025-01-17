<template>
  <div class="dataset-list-container p-24" style="padding-top: 16px">
    <div class="flex-between mb-16">
      <h2>我的知识库</h2>
      <div class="flex-between">
        <el-select
          v-model="selectUserId"
          class="mr-12"
          @change="searchHandle"
          v-show="false"
          style="max-width: 240px; width: 150px"
        >
          <el-option
            v-for="item in userOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-input
          v-model="searchValue"
          @change="searchHandle"
          :placeholder="$t('views.application.applicationList.searchBar.placeholder')"
          prefix-icon="Search"
          class="w-240 mr-12"
          style="max-width: 240px"
          clearable
        />
        <el-button @click="openCreateDialog" 
        type="primary">创建知识库</el-button>

      </div>
    </div>
    <div v-loading.fullscreen.lock="paginationConfig.current_page === 1 && loading">
      <InfiniteScroll
        :size="datasetList.length"
        :total="paginationConfig.total"
        :page_size="paginationConfig.page_size"
        v-model:current_page="paginationConfig.current_page"
        @load="getList"
        :loading="loading"
      >
        <el-row :gutter="15">
          <template v-for="(item, index) in datasetList" :key="index">
            <el-col :xs="24" :sm="12" :md="8" :lg="6" :xl="6" class="mb-16">
              <CardBox
                :title="item.name"
                :description="item.desc"
                class="cursor"
                @click="router.push({ path: `/dataset/${item.id}/document` })"
              >
                <template #icon>
                  <AppAvatar
                    v-if="item.type === '1'"
                    class="mr-8 avatar-purple"
                    shape="square"
                    :size="32"
                  >
                    <img src="@/assets/icon_web.svg" style="width: 58%" alt="" />
                  </AppAvatar>
                  <AppAvatar v-else class="mr-8 avatar-blue" shape="square" :size="32">
                    <img src="@/assets/icon_document.svg" style="width: 58%" alt="" />
                  </AppAvatar>
                </template>
                <div class="delete-button">
                  <el-tag class="blue-tag" v-if="item.type === '0'" style="height: 22px"
                    >通用知识库</el-tag
                  >
                  <el-tag
                    class="purple-tag"
                    v-else-if="item.type === '1'"
                    type="warning"
                    style="height: 22px"
                    >Web站点知识库</el-tag
                  >
                </div>

                <template #footer>
                  <div class="footer-content flex-between">
                    <div>
                      <span >{{ item.username}}</span>
                      <el-divider direction="vertical" />
                      <span >{{ item?.document_count || 0 }}</span>
                      文档<el-divider direction="vertical" />
                      <span >{{ item?.application_mapping_count || 0 }}</span>
                      关联应用
                    </div>
                    <div @click.stop>
                      <el-dropdown trigger="click">
                        <el-button text @click.stop>
                          <el-icon><MoreFilled /></el-icon>
                        </el-button>
                        <template #dropdown>
                          <el-dropdown-menu>
                            <el-dropdown-item
                              icon="Setting"
                              @click.stop="router.push({ path: `/dataset/${item.id}/setting` })"
                            >
                              设置</el-dropdown-item
                            >
                            <el-dropdown-item icon="Delete" @click.stop="deleteDataset(item)"
                              >删除</el-dropdown-item
                            >
                          </el-dropdown-menu>
                        </template>
                      </el-dropdown>
                    </div>
                  </div>
                </template>
              </CardBox>
            </el-col>
          </template>
        </el-row>
      </InfiniteScroll>
    </div>
    <SyncWebDialog ref="SyncWebDialogRef" @refresh="refresh" />
    <CreateDatasetDialog ref="CreateDatasetDialogRef" />
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, reactive, computed } from 'vue'
import SyncWebDialog from '@/views/dataset/component/SyncWebDialog.vue'
import CreateDatasetDialog from './component/CreateDatasetDialog.vue'
import datasetApi from '@/api/dataset'
import { MsgSuccess, MsgConfirm } from '@/utils/message'
import { useRouter } from 'vue-router'
import { numberFormat } from '@/utils/utils'
import { ValidType, ValidCount } from '@/enums/common'
import useStore from '@/stores'
import applicationApi from '@/api/application'

const { user, common } = useStore()
const router = useRouter()

const CreateDatasetDialogRef = ref()
const SyncWebDialogRef = ref()
const loading = ref(false)
const datasetList = ref<any[]>([])
const paginationConfig = reactive({
  current_page: 1,
  page_size: 30,
  total: 0
})

const searchValue = ref('')

interface UserOption {
  label: string
  value: string
}

const userOptions = ref<UserOption[]>([])

const selectUserId = ref('all')

function openCreateDialog() {
  CreateDatasetDialogRef.value.open()

}

function refresh() {
  MsgSuccess('同步任务发送成功')
}

function reEmbeddingDataset(row: any) {
  datasetApi.putReEmbeddingDataset(row.id).then(() => {
    MsgSuccess('提交成功')
  })
}

function syncDataset(row: any) {
  SyncWebDialogRef.value.open(row.id)
}

function searchHandle() {
  if (user.userInfo) {
    localStorage.setItem(user.userInfo.id + 'dataset', selectUserId.value)
  }
  paginationConfig.current_page = 1
  datasetList.value = []
  getList()
}
const export_dataset = (item: any) => {
  datasetApi.exportDataset(item.name, item.id, loading).then((ok) => {
    MsgSuccess('导出成功')
  })
}
const export_zip_dataset = (item: any) => {
  datasetApi.exportZipDataset(item.name, item.id, loading).then((ok) => {
    MsgSuccess('导出成功')
  })
}

function deleteDataset(row: any) {
  MsgConfirm(
    `删除警告`,
    `“${row.name}” 知识库关联 ${row.application_mapping_count} 个应用，删除后无法恢复，请确认！`,
    {
      confirmButtonText: '删除',
      confirmButtonClass: 'danger'
    }
  )
    .then(() => {
      datasetApi.delDataset(row.id, loading).then(() => {
        const index = datasetList.value.findIndex((v) => v.id === row.id)
        datasetList.value.splice(index, 1)
        MsgSuccess('删除成功')
      })
    })
    .catch(() => {})
}

function getList() {
  const params = {
    ...(searchValue.value && { name: searchValue.value }),
    ...(selectUserId.value &&
      selectUserId.value !== 'all' && { select_user_id: selectUserId.value })
  }
  datasetApi.getDataset(paginationConfig, params, loading).then((res) => {
    res.data.records.forEach((item: any) => {
      if (user.userInfo && item.user_id === user.userInfo.id) {
        item.username = user.userInfo.username
      } else {
        item.username = userOptions.value.find((v) => v.value === item.user_id)?.label
      }
    })
    paginationConfig.total = res.data.total
    datasetList.value = [...datasetList.value, ...res.data.records]
  })
}

function getUserList() {
  applicationApi.getUserList('DATASET', loading).then((res) => {
    if (res.data) {
      userOptions.value = res.data.map((item: any) => {
        return {
          label: item.username,
          value: item.id
        }
      })
      if (user.userInfo) {
        const selectUserIdValue = localStorage.getItem(user.userInfo.id + 'dataset')
        if (selectUserIdValue && userOptions.value.find((v) => v.value === selectUserIdValue)) {
          selectUserId.value = selectUserIdValue
        }
      }
      getList()
    }
  })
}

onMounted(() => {
  getUserList()
})
</script>
<style lang="scss" scoped>
.dataset-list-container {
  .delete-button {
    position: absolute;
    right: 12px;
    top: 15px;
    height: auto;
  }
  .footer-content {
    .bold {
      color: var(--app-text-color);
    }
  }
  :deep(.el-divider__text) {
    background: var(--app-layout-bg-color);
  }
}
</style>
