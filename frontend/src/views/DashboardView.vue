<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Дашборд</h2>
    <div v-if="store.loading" class="text-gray-500">Загрузка...</div>
    <div v-else-if="store.data" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-700">Avito</h3>
        <div class="mt-2 space-y-1">
          <p>Аккаунтов: <span class="font-bold">{{ store.data.avito.accounts }}</span></p>
          <p>Объявлений: <span class="font-bold">{{ store.data.avito.total_ads }}</span></p>
          <p>Активных: <span class="font-bold text-green-600">{{ store.data.avito.active_ads }}</span></p>
        </div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-700">Контакты</h3>
        <div class="mt-2 space-y-1">
          <p>Всего: <span class="font-bold">{{ store.data.contacts.total }}</span></p>
          <p>Подписчиков: <span class="font-bold text-green-600">{{ store.data.contacts.subscribed }}</span></p>
        </div>
      </div>
      <div class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-semibold text-gray-700">Email</h3>
        <div class="mt-2 space-y-1">
          <p>Кампаний: <span class="font-bold">{{ store.data.email.total_campaigns }}</span></p>
          <p>Отправлено: <span class="font-bold text-blue-600">{{ store.data.email.sent_campaigns }}</span></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDashboardStore } from '../store'
const store = useDashboardStore()
onMounted(() => store.fetch())
</script>
