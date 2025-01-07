<template>
  <div class="top-menu-container flex align-center h-full"
  style="border-radius: 20px; background-color: #ebe9e9; height: 80%;">
    <MenuItem
      :menu="menu"
      v-hasPermission="menu.meta?.permission"
      v-for="(menu, index) in topMenuList"
      :key="index"
    >
    </MenuItem>
  </div>
</template>
<script setup lang="ts">
import { computed } from 'vue'
import { getChildRouteListByPathAndName } from '@/router/index'
import MenuItem from './MenuItem.vue'

const topMenuList = computed(() => {
  var tMenuList = getChildRouteListByPathAndName('/', 'home')
                    .filter(v => v.name !== 'setting')
  return tMenuList
})
</script>
<style lang="scss" scope>

</style>
