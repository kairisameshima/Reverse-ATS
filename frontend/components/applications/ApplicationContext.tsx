'use client'

import React, { createContext, useState, useContext, useEffect } from 'react'
import { format, differenceInDays, parseISO } from 'date-fns'

type Stage = {
  name: string
  scheduledDate: string
  occurredDate: string
  notes: string
  status: "scheduled" | "completed" | "rejected" | "pending"
}

type Application = {
  uuid: string
  company: string
  position: string
  status: "prospect" | "applied" | "interviewing" | "offered" | "accepted" | "rejected"
  dateApplied: string
  dateFirstResponse: string
  dateRejected: string
  stages: Stage[]
  lastUpdated: string
}

type ApplicationContextType = {
  applications: Application[]
  addApplication: (newApp: Omit<Application, 'id' | 'stages' | 'lastUpdated' | 'dateFirstResponse' | 'dateRejected'>) => Promise<void>
  updateApplicationStatus: (id: number, status: Application['status']) => Promise<void>
  updateStage: (applicationId: number, stageName: string, updates: Partial<Stage>) => Promise<void>
  deleteApplication: (id: number) => Promise<void>
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
      const response = await fetch(API_URL)
      if (!response.ok) {
        throw new Error('Failed to fetch applications')
      }
      const data = await response.json()
      setApplications(data)
    } catch (error) {
      console.error('Error fetching applications:', error)
    }
  }

  const addApplication = async (newApp: Omit<Application, 'id' | 'stages' | 'lastUpdated' | 'dateFirstResponse' | 'dateRejected'>) => {
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
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

  const updateApplicationStatus = async (id: number, status: Application["status"]) => {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
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

  const updateStage = async (applicationId: number, stageName: string, updates: Partial<Stage>) => {
    try {
      const response = await fetch(`${API_URL}/${applicationId}/stages/${stageName}`, {
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

  const deleteApplication = async (id: number) => {
    try {
      const response = await fetch(`${API_URL}/${id}`, {
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
    const lastUpdate = new Date(app.lastUpdated)
    return differenceInDays(new Date(), lastUpdate) >= 5
  }

  const prepareChartData = () => {
    const data: { [key: string]: { [key: string]: number } } = {}
    applications.forEach(app => {
      const appliedDate = format(parseISO(app.dateApplied), 'yyyy-MM-dd')
      if (!data[appliedDate]) {
        data[appliedDate] = {}
      }
      app.stages.forEach(stage => {
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