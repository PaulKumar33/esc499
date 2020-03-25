///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Jun 17 2015)
// http://www.wxformbuilder.org/
//
// PLEASE DO "NOT" EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#include "noname.h"

///////////////////////////////////////////////////////////////////////////

MyFrame1::MyFrame1( wxWindow* parent, wxWindowID id, const wxString& title, const wxPoint& pos, const wxSize& size, long style ) : wxFrame( parent, id, title, pos, size, style )
{
	this->SetSizeHints( wxDefaultSize, wxDefaultSize );
	
	wxBoxSizer* bMainSizer;
	bMainSizer = new wxBoxSizer( wxVERTICAL );
	
	m_notebook5 = new wxNotebook( this, wxID_ANY, wxDefaultPosition, wxDefaultSize, 0 );
	pHome = new wxPanel( m_notebook5, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL );
	m_notebook5->AddPage( pHome, wxT("Home"), false );
	pTime_freq = new wxPanel( m_notebook5, wxID_ANY, wxDefaultPosition, wxDefaultSize, wxTAB_TRAVERSAL );
	wxBoxSizer* bTimeFreqDomain;
	bTimeFreqDomain = new wxBoxSizer( wxVERTICAL );
	
	wxBoxSizer* bTimeDomain;
	bTimeDomain = new wxBoxSizer( wxHORIZONTAL );
	
	
	bTimeFreqDomain->Add( bTimeDomain, 1, wxEXPAND, 5 );
	
	wxBoxSizer* bFreqDomain;
	bFreqDomain = new wxBoxSizer( wxHORIZONTAL );
	
	
	bTimeFreqDomain->Add( bFreqDomain, 1, wxEXPAND, 5 );
	
	
	pTime_freq->SetSizer( bTimeFreqDomain );
	pTime_freq->Layout();
	bTimeFreqDomain->Fit( pTime_freq );
	m_notebook5->AddPage( pTime_freq, wxT("Time/Freq Analysis"), true );
	
	bMainSizer->Add( m_notebook5, 1, wxEXPAND | wxALL, 5 );
	
	
	this->SetSizer( bMainSizer );
	this->Layout();
	m_menubar1 = new wxMenuBar( 0 );
	mFile = new wxMenu();
	wxMenuItem* mSave;
	mSave = new wxMenuItem( mFile, wxID_ANY, wxString( wxT("Save") ) , wxEmptyString, wxITEM_NORMAL );
	mFile->Append( mSave );
	
	wxMenuItem* mLoad;
	mLoad = new wxMenuItem( mFile, wxID_ANY, wxString( wxT("Load") ) , wxEmptyString, wxITEM_NORMAL );
	mFile->Append( mLoad );
	
	m_menubar1->Append( mFile, wxT("FIle") ); 
	
	mView = new wxMenu();
	wxMenuItem* mTest;
	mTest = new wxMenuItem( mView, wxID_ANY, wxString( wxT("Test Signal") ) , wxEmptyString, wxITEM_NORMAL );
	mView->Append( mTest );
	
	wxMenuItem* mReport;
	mReport = new wxMenuItem( mView, wxID_ANY, wxString( wxT("Report") ) , wxEmptyString, wxITEM_NORMAL );
	mView->Append( mReport );
	
	m_menubar1->Append( mView, wxT("View") ); 
	
	this->SetMenuBar( m_menubar1 );
	
	
	this->Centre( wxBOTH );
}

MyFrame1::~MyFrame1()
{
}
