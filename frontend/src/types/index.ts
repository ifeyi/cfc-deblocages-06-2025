// ============================
// frontend/src/types/index.ts
// ============================
export interface Client {
  id: number
  client_number: string
  name: string
  company_name?: string
  address: string
  phone: string
  email?: string
  id_card_number?: string
  is_active: boolean
  created_at: string
  updated_at?: string
}

export interface Loan {
  id: number
  loan_number: string
  client_id: number
  loan_type: LoanType
  status: LoanStatus
  amount: string
  duration_months: number
  grace_period_months: number
  interest_rate: string
  monthly_payment: string
  approval_date?: string
  signature_date?: string
  first_payment_date?: string
  validity_end_date?: string
  mortgage_amount?: string
  property_title_number?: string
  property_location?: string
  life_insurance_company?: string
  fire_insurance_company?: string
  created_at: string
  updated_at?: string
  client?: Client
  disbursements?: Disbursement[]
  alerts?: Alert[]
}

export enum LoanType {
  CLASSIC_ACQUIRER = 'PRET_CLASSIQUE_ACQUEREUR',
  CLASSIC_BUILDER = 'PRET_CLASSIQUE_CONSTRUCTEUR',
  RENTAL_ORDINARY = 'PRET_LOCATIF_ORDINAIRE',
  YOUNG_LAND = 'FONCIER_CLASSIQUE_JEUNES',
}

export enum LoanStatus {
  DRAFT = 'BROUILLON',
  APPROVED = 'APPROUVE',
  IN_PROGRESS = 'EN_COURS',
  DISBURSING = 'DEBLOCAGE',
  COMPLETED = 'COMPLETE',
  CANCELLED = 'ANNULE',
  SUSPENDED = 'SUSPENDU',
}

export interface Disbursement {
  id: number
  loan_id: number
  disbursement_number: number
  status: DisbursementStatus
  requested_amount: string
  approved_amount?: string
  disbursed_amount?: string
  request_date: string
  approval_date?: string
  disbursement_date?: string
  work_description: string
  work_completion_percentage: number
  site_visit_date?: string
  site_visit_report?: string
  bet_name?: string
  bet_report_received: boolean
  created_at: string
  updated_at?: string
}

export enum DisbursementStatus {
  REQUESTED = 'DEMANDE',
  APPROVED = 'APPROUVE',
  IN_PROGRESS = 'EN_COURS',
  COMPLETED = 'COMPLETE',
  REJECTED = 'REJETE',
  SUSPENDED = 'SUSPENDU',
}

export interface Alert {
  id: number
  loan_id: number
  alert_type: AlertType
  status: AlertStatus
  severity: 'ORANGE' | 'RED'
  message: string
  triggered_at: string
  acknowledged_at?: string
  resolved_at?: string
  email_sent: boolean
  sms_sent: boolean
  loan?: Loan
}

export enum AlertType {
  VALIDITY_WARNING = 'VALIDITY_WARNING',
  VALIDITY_CRITICAL = 'VALIDITY_CRITICAL',
  WORK_DELAY_WARNING = 'WORK_DELAY_WARNING',
  WORK_DELAY_CRITICAL = 'WORK_DELAY_CRITICAL',
  REPAYMENT_UPCOMING = 'REPAYMENT_UPCOMING',
  REPAYMENT_IMMINENT = 'REPAYMENT_IMMINENT',
  MISSING_DOCUMENT = 'MISSING_DOCUMENT',
  DOCUMENT_EXPIRY = 'DOCUMENT_EXPIRY',
}

export enum AlertStatus {
  PENDING = 'PENDING',
  ACKNOWLEDGED = 'ACKNOWLEDGED',
  RESOLVED = 'RESOLVED',
  ESCALATED = 'ESCALATED',
}