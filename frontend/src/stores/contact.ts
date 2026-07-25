import { defineStore } from 'pinia'
import { ref } from 'vue'
import { contactApi, type ContactContent } from '@/api/modules/contact'

export const useContactStore = defineStore('contact', () => {
  const content = ref<ContactContent | null>(null)
  const loading = ref(false)

  const fetchContact = async () => {
    loading.value = true
    try {
      content.value = await contactApi.getContact()
      return content.value
    } finally {
      loading.value = false
    }
  }

  const updateContact = async (data: ContactContent) => {
    content.value = await contactApi.updateContact(data)
    return content.value
  }

  return {
    content,
    loading,
    fetchContact,
    updateContact,
  }
})
