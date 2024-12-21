'use client'

import { ApplicationProvider } from '../../components/applications/ApplicationContext'
import ApplicantTrackingSystem from '../../components/applications/ApplicantTrackingSystem'

export function ApplicationsPage() {
  return (
    <ApplicationProvider>
      <ApplicantTrackingSystem />
    </ApplicationProvider>
  )
}

export default ApplicationsPage;