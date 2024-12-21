'use client'

import { differenceInDays, format, parseISO } from 'date-fns'
import React, { createContext, useContext, useEffect, useState } from 'react'

type Stage = {
  name: string
  scheduledDate: string
  occurredDate: string
  notes: string
  status: "scheduled" | "completed" | "rejected" | "pending"
}

type Application = {
  uuid: string
  create_date: string
  update_date: string
  company: string
  description: string | null
  user_uuid: string
  position: string
  status: "prospect" | "applied" | "interviewing" | "offered" | "accepted" | "rejected"
  date_applied: string
  date_first_response: string | null
  date_rejected: string | null
  stages?: Stage[] // We'll keep this optional for now
}

type ApplicationContextType = {
  applications: Application[]
  addApplication: (newApp: Omit<Application, 'uuid' | 'create_date' | 'update_date' | 'user_uuid' | 'stages'>) => Promise<void>
  updateApplicationStatus: (uuid: string, status: Application['status']) => Promise<void>
  updateStage: (applicationUuid: string, stageName: string, updates: Partial<Stage>) => Promise<void>
  deleteApplication: (uuid: string) => Promise<void>
  shouldFollowUp: (app: Application) => boolean
  prepareChartData: () => { date: string; [key: string]: number }[]
}

const ApplicationContext = createContext<ApplicationContextType | undefined>(undefined)

const API_URL = 'http://localhost:8000/applications'

export const ApplicationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [applications, setApplications] = useState<Application[]>([])

  useEffect(() => {
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    try {
      const authToken = document.cookie.split('; ').find(row => row.startsWith('authToken=')).split('=')[1]
      const response = await fetch(API_URL, {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      })
      if (!response.ok) {
        throw new Error('Failed to fetch applications')
      }
      const data = await response.json()
      setApplications(data)
    } catch (error) {
      console.error('Error fetching applications:', error)
    }
  }

  const addApplication = async (newApp: Omit<Application, 'uuid' | 'create_date' | 'update_date' | 'user_uuid' | 'stages'>) => {
    try {
      const authToken = document.cookie.split('; ').find(row => row.startsWith('authToken=')).split('=')[1]
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify(newApp),
      })
      if (!response.ok) {
        throw new Error('Failed to add application')
      }
      await fetchApplications()
    } catch (error) {
      console.error('Error adding application:', error)
    }
  }

  const updateApplicationStatus = async (uuid: string, status: Application["status"]) => {
    try {
      const response = await fetch(`${API_URL}/${uuid}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status }),
      })
      if (!response.ok) {
        throw new Error('Failed to update application status')
      }
      await fetchApplications()
    } catch (error) {
      console.error('Error updating application status:', error)
    }
  }

  const updateStage = async (applicationUuid: string, stageName: string, updates: Partial<Stage>) => {
    try {
      const response = await fetch(`${API_URL}/${applicationUuid}/stages/${stageName}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updates),
      })
      if (!response.ok) {
        throw new Error('Failed to update stage')
      }
      await fetchApplications()
    } catch (error) {
      console.error('Error updating stage:', error)
    }
  }

  const deleteApplication = async (uuid: string) => {
    try {
      const response = await fetch(`${API_URL}/${uuid}`, {
        method: 'DELETE',
      })
      if (!response.ok) {
        throw new Error('Failed to delete application')
      }
      await fetchApplications()
    } catch (error) {
      console.error('Error deleting application:', error)
    }
  }

  const shouldFollowUp = (app: Application) => {
    const lastUpdate = new Date(app.update_date)
    return differenceInDays(new Date(), lastUpdate) >= 5
  }

  const prepareChartData = () => {
    const data: { [key: string]: { [key: string]: number } } = {}
    applications.forEach(app => {
      const appliedDate = format(parseISO(app.date_applied), 'yyyy-MM-dd')
      if (!data[appliedDate]) {
        data[appliedDate] = {}
      }
      app.stages?.forEach(stage => {
        if (stage.occurredDate) {
          const stageName = stage.name.replace(/\s+/g, '')
          data[appliedDate][stageName] = (data[appliedDate][stageName] || 0) + 1
        }
      })
    })
    return Object.entries(data).map(([date, stages]) => ({
      date,
      ...stages
    }))
  }

  return (
    <ApplicationContext.Provider value={{ 
      applications, 
      addApplication, 
      updateApplicationStatus, 
      updateStage, 
      deleteApplication, 
      shouldFollowUp,
      prepareChartData
    }}>
      {children}
    </ApplicationContext.Provider>
  )
}

export const useApplicationContext = () => {
  const context = useContext(ApplicationContext)
  if (context === undefined) {
    throw new Error('useApplicationContext must be used within an ApplicationProvider')
  }
  return context
}

export default ApplicationContext;