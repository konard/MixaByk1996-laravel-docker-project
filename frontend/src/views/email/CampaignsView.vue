<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Email кампании</h2>
      <button @click="showForm = !showForm" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        {{ showForm ? 'Отмена' : '+ Создать' }}
      </button>
    </div>

    <form v-if="showForm" @submit.prevent="add" class="bg-white p-4 rounded shadow mb-6 space-y-3">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input v-model="form.name" placeholder="Название кампании" class="border rounded p-2" required />
        <input v-model="form.subject" placeholder="Тема письма (вариант A)" class="border rounded p-2" required />
        <input v-model="form.subject_b" placeholder="Тема письма (вариант B, для A/B теста)" class="border rounded p-2" />
        <select v-model="form.template_id" class="border rounded p-2">
          <option value="">Выберите шаблон</option>
          <option v-for="t in emailStore.templates" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
        <select v-model="form.segment_id" class="border rounded p-2">
          <option value="">Выберите сегмент</option>
          <option v-for="s in contactStore.segments" :key="s.id" :value="s.id">{{ s.name }}</option>
        </select>
        <select v-model="form.recurrence" class="border rounded p-2">
          <option value="">Без повтора</option>
          <option value="daily">Ежедневно</option>
          <option value="weekly">Еженедельно</option>
          <option value="monthly">Ежемесячно</option>
        </select>
      </div>
      <button type="submit" class="bg-green-600 text-white px-4 py-2 rounded">Создать</button>
    </form>

    <div class="bg-white rounded shadow overflow-hidden">
      <table class="w-full text-left">
        <thead class="bg-gray-50"><tr><th class="p-3">ID</th><th class="p-3">Название</th><th class="p-3">Тема</th><th class="p-3">Статус</th><th class="p-3">Отправлено</th><th class="p-3">Открыто</th><th class="p-3">Клики</th><th class="p-3">Действия</th></tr></thead>
        <tbody>
          <tr v-for="c in emailStore.campaigns" :key="c.id" class="border-t">
            <td class="p-3">{{ c.id }}</td>
            <td class="p-3">{{ c.name }}</td>
            <td class="p-3">{{ c.subject }}</td>
            <td class="p-3"><span class="px-2 py-1 rounded text-xs" :class="{'bg-green-100 text-green-700': c.status === 'sent', 'bg-gray-100': c.status === 'draft', 'bg-blue-100 text-blue-700': c.status === 'sending'}">{{ c.status }}</span></td>
            <td class="p-3">{{ c.sent_count }}</td>
            <td class="p-3">{{ c.open_count }}</td>
            <td class="p-3">{{ c.click_count }}</td>
            <td class="p-3">
              <button v-if="c.status === 'draft' || c.status === 'scheduled'" @click="emailStore.sendCampaign(c.id)" class="text-blue-600 hover:underline">Отправить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEmailStore, useContactStore } from '../../store'
const emailStore = useEmailStore()
const contactStore = useContactStore()
const showForm = ref(false)
const form = ref({ name: '', subject: '', subject_b: '', template_id: '', segment_id: '', recurrence: '' })
const add = async () => {
  const data = { ...form.value }
  if (!data.template_id) delete data.template_id
  if (!data.segment_id) delete data.segment_id
  if (!data.subject_b) delete data.subject_b
  if (!data.recurrence) delete data.recurrence
  await emailStore.createCampaign(data)
  form.value = { name: '', subject: '', subject_b: '', template_id: '', segment_id: '', recurrence: '' }
  showForm.value = false
}
onMounted(() => { emailStore.fetchCampaigns(); emailStore.fetchTemplates(); contactStore.fetchSegments() })
</script>
